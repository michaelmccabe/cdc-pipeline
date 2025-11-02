import json
import logging
import argparse
from redis import Redis

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Redis connection
r = Redis(host='localhost', port=6379, decode_responses=True)
stream_name = 'cdc-server.test_schema.employee'

def log_event(msg_id, op, after=None, before=None):
    """Log every event."""
    after_str = json.dumps(after, indent=2) if after else 'N/A'
    before_str = json.dumps(before, indent=2) if before else 'N/A'
    logger.info(f"Event ID {msg_id}: op='{op}' | After:\n{after_str} | Before:\n{before_str}")
    if op in ('c', 'r'):
        logger.info(f"  -> CREATE: New employee (ID {msg_id})")
    elif op == 'u':
        logger.info(f"  -> UPDATE: Changed (ID {msg_id})")
    elif op == 'd':
        logger.info(f"  -> DELETE: Removed (ID {msg_id})")
    else:
        logger.warning(f"  -> Unknown op '{op}' (ID {msg_id}): Skipping")

def parse_message(msg_data):
    """Parse Debezium format."""
    op = None
    after = None
    before = None
    
    if len(msg_data) == 1:
        try:
            _, value_str = list(msg_data.items())[0]
            envelope = json.loads(value_str)
            payload = envelope.get('payload', {})
            op = payload.get('op')
            after = payload.get('after')
            before = payload.get('before')
        except (json.JSONDecodeError, KeyError) as e:
            logger.debug(f"Parse error: {e}")
    else:
        op = msg_data.get('__debezium_op') or msg_data.get('op')
        after_str = msg_data.get('__debezium_after') or msg_data.get('after')
        before_str = msg_data.get('__debezium_before') or msg_data.get('before')
        try:
            after = json.loads(after_str) if after_str else None
            before = json.loads(before_str) if before_str else None
        except json.JSONDecodeError:
            pass
    
    return op, after, before

def consume_all():
    """Process all entries in stream."""
    logger.info(f"Processing ALL entries from stream: {stream_name}")
    try:
        entries = r.xrange(stream_name, min='-', max='+')
        processed = 0
        for msg_id, msg_data in entries:
            op, after, before = parse_message(msg_data)
            if op:
                log_event(msg_id, op, after, before)
                processed += 1
        logger.info(f"Processed {processed} total events.")
    except Exception as e:
        logger.error(f"Read error: {e}")

def tail_new():
    """Tail new entries."""
    last_id = '$'
    logger.info(f"Tailing new entries from ID: {last_id}")
    while True:
        try:
            messages = r.xread({stream_name: last_id}, block=5000, count=None)
            if not messages:
                continue
            
            for stream, msgs in messages:
                for msg_id, msg_data in msgs:
                    op, after, before = parse_message(msg_data)
                    if op:
                        log_event(msg_id, op, after, before)
                    last_id = msg_id  # Sequential for next
        except KeyboardInterrupt:
            logger.info("Stopped.")
            break
        except Exception as e:
            logger.error(f"Error: {e}")
            import time
            time.sleep(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--all', action='store_true', help='Process all historical entries')
    args = parser.parse_args()
    
    try:
        info = r.xinfo_stream(stream_name)
        logger.info(f"Stream '{stream_name}' ready: {info.get('length', 0)} total entries")
    except Exception as e:
        logger.warning(f"Stream check failed: {e}")
    
    logger.info(f"Starting consumer for stream: {stream_name}")
    if args.all:
        consume_all()
    else:
        consume_all()  # Always process historical first
        tail_new()