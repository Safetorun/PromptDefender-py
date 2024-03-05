from wall_builder import create_wall

print(
    create_wall(
        xml_tag="xml_tag",
        remote_jailbreak_check=True
    ).execute_validators("Hello, this is a safe prompt")
)
