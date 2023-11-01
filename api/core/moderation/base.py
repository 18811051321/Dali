from abc import abstractmethod, ABC
from core.extension.extensible import Extensible


class Moderation(ABC, Extensible):

    @classmethod
    @abstractmethod
    def validate_config(cls, config: dict) -> None:
        pass

    @classmethod
    @abstractmethod
    def moderation_for_inputs(cls, tenant_id: str, config: dict, inputs: dict, query: str):
        pass

    @classmethod
    @abstractmethod
    def moderation_for_output(cls, tenant_id: str, config: dict, output: str):
        pass

    @classmethod
    def _validate_inputs_and_outputs_config(cls, config: dict, is_preset_response_required: bool) -> None:
        # inputs_configs
        inputs_configs = config.get("inputs_configs")
        if not isinstance(inputs_configs, dict):
            raise ValueError("inputs_configs must be a dict")
        
        # outputs_configs
        outputs_configs = config.get("outputs_configs")
        if not isinstance(outputs_configs, dict):
            raise ValueError("outputs_configs must be a dict")

        inputs_configs_enabled = inputs_configs.get("enabled")
        outputs_configs_enabled = outputs_configs.get("enabled")
        if not inputs_configs_enabled and not outputs_configs_enabled:
            raise ValueError("At least one of inputs_configs or outputs_configs must be enabled")

        # preset_response
        if not is_preset_response_required:
            return
        
        if inputs_configs_enabled and not inputs_configs.get("preset_response"):
            raise ValueError("inputs_configs.preset_response is required")
        
        if outputs_configs_enabled and not outputs_configs.get("preset_response"):
            raise ValueError("outputs_configs.preset_response is required")

class ModerationException(Exception):
    pass