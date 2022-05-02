import os, fnmatch, csv
key_words = ['@NamedAction', '@TasyFeature', '@TasyFront', '@W', 'extends WhebAction', 'extends DefaultCommand', '@Path(' ]
folder_path_directory_root = 'C:\\dev\\git\\tasy-backend'
extesion = '*.java'
csv_header = ['module', 'submodule', 'annotation', 'code']
csv_data = []

def generate_csv():
    csv_file_name = 'modules.csv'
    if os.path.exists(csv_file_name):
        os.remove(csv_file_name)

    with open(csv_file_name, 'w', encoding='UTF8', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(csv_header)
        csv_writer.writerows(csv_data)

def search_multiple_strings_in_file(file_name):
    """Get line from the file along with line numbers, which contains any string from the list"""
    line_number = 0
    list_of_results = []
    # Open the file in read only mode
    with open(file_name, 'r', encoding="utf8", errors="ignore") as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            line_number += 1
            # For each line, check if line contains any string from the list of strings
            for string_to_search in key_words:
                if string_to_search in line:
                    # If any string is found in line, then append that line along with line number in list
                    list_of_results.append((string_to_search, line_number, line.rstrip()))
    # Return list of tuples containing matched string, line numbers and lines where string is found
    return list_of_results
        
def find_in_file(fileDirectory):
    matched_lines = search_multiple_strings_in_file(fileDirectory)
    # print('Total Matched lines : ', len(matched_lines))

    for elem in matched_lines:
        # print('Word = ', elem[0], ' :: Line Number = ', elem[1], ' :: Line = ', elem[2])
        module = fileDirectory.replace(folder_path_directory_root + '\\', '')
        directory_array = module.split('\\')
        directory_array = [each_string.lower() for each_string in directory_array]
        module = directory_array[0]
        directory_array.reverse()
        submodule_index = directory_array.index(module) - 1
        submodule = directory_array[submodule_index]
        csv_line = [module, submodule, elem[0], elem[2]]
        csv_data.append(csv_line)


def find_files_by_extension(folder_path_directory, pattern):
    dir_number = 0
    for root, dirs, files in os.walk(folder_path_directory):
        dir_number += 1
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename


for filename in find_files_by_extension(folder_path_directory_root, extesion):
    find_in_file(filename)
generate_csv()
