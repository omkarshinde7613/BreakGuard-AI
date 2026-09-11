from breakguard.parser import get_endpoints


def diff_schemas(old_schema: dict, new_schema: dict) -> list[dict]:
    old_endpoints = get_endpoints(old_schema)
    new_endpoints = get_endpoints(new_schema)

    changes = []

    removed = old_endpoints.keys() - new_endpoints.keys()
    for endpoint in removed:
        changes.append({"type": "endpoint_removed", "endpoint": endpoint})

    added = new_endpoints.keys() - old_endpoints.keys()
    for endpoint in added:
        changes.append({"type": "endpoint_added", "endpoint": endpoint})

    common = old_endpoints.keys() & new_endpoints.keys()
    for endpoint in common:
        param_changes = _diff_parameters(
            old_endpoints[endpoint].get("parameters", []),
            new_endpoints[endpoint].get("parameters", []),
        )
        for change in param_changes:
            change["endpoint"] = endpoint
            changes.append(change)

    return changes


def _diff_parameters(old_params: list, new_params: list) -> list[dict]:
    changes = []
    old_by_name = {p["name"]: p for p in old_params}
    new_by_name = {p["name"]: p for p in new_params}

    for name, old_param in old_by_name.items():
        new_param = new_by_name.get(name)
        if new_param is None:
            changes.append({"type": "parameter_removed", "parameter": name})
            continue

        old_type = old_param.get("schema", {}).get("type")
        new_type = new_param.get("schema", {}).get("type")
        if old_type != new_type:
            changes.append({
                "type": "parameter_type_changed",
                "parameter": name,
                "old_type": old_type,
                "new_type": new_type,
            })

    return changes