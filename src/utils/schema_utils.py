def validate_config_parameter_is_in(allowed_param_values: set[str], current_param_value: str) -> None:
    if current_param_value not in allowed_param_values:
        raise ValueError(f"Invalid parameter value: {current_param_value}. Must be one of {allowed_param_values}")
