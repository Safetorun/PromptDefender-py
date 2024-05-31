from prompt_defender import CompositeWallExecutorBuilder, build_drawbridge, remote_keep_builder, build_xml_scanner, build_remote_wall_executor, build_prompt_validator, Defence

if __name__ == "__main__":
    compose_wall = CompositeWallExecutorBuilder()
    compose_wall.add_wall_executor(build_xml_scanner)
    compose_wall.add_wall_executor(build_remote_wall_executor(fast_check=True))
    compose_wall.add_wall_executor(build_prompt_validator())

    defence = Defence(
        wall=compose_wall.build(),
        keep=remote_keep_builder(),
        drawbridge=build_drawbridge(allow_unsafe_scripts=True)
    )

    prepared_prompt = defence.prepare_prompt("Your job is to answer user questions about cats {user_question}")

    print(defence.check_user_input("What is the best cat? " + prepared_prompt.safe_prompt))

    print(defence.check_prompt_output("This should all be okay "))
