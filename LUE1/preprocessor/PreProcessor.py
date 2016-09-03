import json,re,sys

class PreProcessor:
    # Performs pre-processing of data
    def pre_process(data_filename, config_filename, output_filename):
        with open(data_filename, 'r') as data_file, open(config_filename, 'r') as config_file, \
                open(output_filename, 'w') as output_filename:
            # Load the regex configuration file
            config = json.load(config_file)
            for line in data_file.readlines():
                # Try to stringify a hashtag if it's in camel case - e.g. #ModiInDubai => Modi In Dubai
                line = camel_case_split(line)
                # Replace all the hashtags with HASHTAG token
                for k, v in config['replace_tokens'].items():
                    line = re.sub(v, k, line)
                for title, icons in config['emoticons'].items():
                    for icon in icons:
                        line = line.replace(icon, title)
                # Remove all the tokens specified in the configuration JSON file.
                for token in config['remove_tokens']:
                    line = re.sub(token, ' ', line)
                output_filename.write(re.sub(r'(\s+)', ' ', line).strip().lower() + '\n')


    # Try to stringify a hashtag if it's in camel case - e.g. #ModiInDubai => Modi In Dubai
    def hashtag_stringify(token):
        matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', token)
        words = [m.group(0) for m in matches]
        return ' '.join(words) if len(words) > 1 else '#' + token


    def camel_case_split(line):
        phrases = []
        for word in re.split(r'\s+', line):
            phrases.append(hashtag_stringify(word[1:]) if len(word) > 0 and word[0] == '#' else word)
        return ' '.join(phrases)


# Arguments : Path to input file, Path to config file, Path to output file
# e.g. python PreProcessor.py tweets.txt preprocess_config.json cleaned_data.txt
if __name__ == '__main__':
    pre_process(sys.argv[1], sys.argv[2], sys.argv[3])
