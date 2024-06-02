import logging
from PyQt5.QtWidgets import QMessageBox

logger = logging.getLogger(__name__)

class FabricError(Exception):
    """Base class for Fabric-related exceptions"""
    pass

class InvalidAPIKeyError(FabricError):
    """Raised when the API key is invalid"""
    pass

class NetworkConnectionError(FabricError):
    """Raised when there is a network connectivity issue"""
    pass

class UnsupportedFileFormatError(FabricError):
    """Raised when the input file format is not supported"""
    pass

class MissingRequiredDataError(FabricError):
    """Raised when required data is missing"""
    pass

class InvalidUserInputError(FabricError):
    """Raised when user input is invalid"""
    pass

def handle_api_key_error(parent_widget=None):
    """Display an error message for invalid API key"""
    logger.error("Invalid API key. Please check your API key and try again.")
    QMessageBox.critical(parent_widget, "Error", "Invalid API key. Please check your API key and try again.")
    raise InvalidAPIKeyError("Invalid API key")

def handle_network_error(parent_widget=None):
    """Display an error message for network connectivity issues"""
    logger.error("Network connection error. Please check your internet connection and try again.")
    QMessageBox.critical(parent_widget, "Error", "Network connection error. Please check your internet connection and try again.")
    raise NetworkConnectionError("Network connection error")

def handle_unsupported_file_format(parent_widget=None):
    """Display an error message for unsupported file formats"""
    logger.error("Unsupported file format. Please try a different file format.")
    QMessageBox.critical(parent_widget, "Error", "Unsupported file format. Please try a different file format.")
    raise UnsupportedFileFormatError("Unsupported file format")

def handle_missing_required_data(parent_widget=None):
    """Display an error message for missing required data"""
    logger.error("Required data is missing. Please ensure all necessary information is provided.")
    QMessageBox.critical(parent_widget, "Error", "Required data is missing. Please ensure all necessary information is provided.")
    raise MissingRequiredDataError("Required data is missing")

def handle_invalid_user_input(parent_widget=None):
    """Display an error message for invalid user input"""
    logger.error("Invalid user input. Please check your input and try again.")
    QMessageBox.critical(parent_widget, "Error", "Invalid user input. Please check your input and try again.")
    raise InvalidUserInputError("Invalid user input")