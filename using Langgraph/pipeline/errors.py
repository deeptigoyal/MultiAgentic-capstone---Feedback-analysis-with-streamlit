class ConfigError(Exception):
    pass

class DataLoadError(Exception):
    pass

class ModelError(Exception):
    pass

class PipelineError(Exception):
    """Graph orchestration / state transition errors"""
    pass

class OutputWriteError(Exception):
    """CSV writing / file system errors"""
    pass
