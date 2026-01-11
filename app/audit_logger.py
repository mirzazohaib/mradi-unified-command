import logging

# Configure the logger to write to a file
logging.basicConfig(
    filename='audit.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_transaction(action: str, mission_id: str, details: str):
    """
    MRADI-6: Standardized audit logging for compliance.
    """
    message = f"Action: {action} | Mission: {mission_id} | Details: {details}"
    logging.info(message)
    print(f"Audit Logged: {message}")