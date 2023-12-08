from zipfile import ZipFile

def update_lambda_code_file(file_name: str, new_topic_arn: str):
    updated_lines = []

    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()

        for line in lines:
            if line.startswith('    topic_arn = '):
                updated_lines.append(f"    topic_arn = '{new_topic_arn}'\n")
            else:
                updated_lines.append(line)

        with open(file_name, 'w') as file:
            file.writelines(updated_lines)

        print(f'lambda code file {file_name} updated with new topic ARN')
    except Exception as E:
        print(f'\tcant update lambda code file {file_name}! {E}')


def create_zip_from_py(file_name: str):
    zip_file_name = file_name.replace('.py', '.zip')
    try:
        with ZipFile(zip_file_name, 'w') as z:
            z.write(file_name)
    except Exception as E:
        print(f'\tCant create lambda zip file {zip_file_name} from {file_name}, {E}')
    print('lambda zip file created')
