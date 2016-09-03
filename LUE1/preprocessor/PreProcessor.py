import json, re, sys

from OrderedSet import OrderedSet


# Performs pre-processing of data
class PreProcessor:
    def __init__(self, config_filename):
        with open(config_filename, 'r') as config_file:
            # Load the regex configuration file
            self.config = json.load(config_file)

    def pre_process(self, data_filename):
        lines = OrderedSet()
        with open(data_filename, 'r') as data_file:
            for line in data_file.readlines():
                # Try to stringify a hashtag if it's in camel case - e.g. #ModiInDubai => Modi In Dubai
                line = self.camel_case_split(line)
                # Replace all the hashtags with HASHTAG token
                for k, v in self.config['replace_tokens'].items():
                    line = re.sub(v, k, line)
                # Replacing the emoticons with their title.
                for title, icons in self.config['emoticons'].items():
                    for icon in icons:
                        line = line.replace(icon, title)
                # Remove all the tokens specified in the configuration JSON file.
                for token in self.config['remove_tokens']:
                    line = re.sub(token, ' ', line)
                line = re.sub(r'(\s+)', ' ', line).strip().lower()
                lines.add(line)
        return lines

    @staticmethod
    def write_file(filename, lines):
        with open(filename, 'w') as output_file:
            for line in lines:
                output_file.write(line + '\n')

    @staticmethod
    # Try to stringify a hashtag if it's in camel case - e.g. #ModiInDubai => Modi In Dubai
    def hashtag_stringify(token):
        matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', token)
        words = [m.group(0) for m in matches]
        return ' '.join(words) if len(words) > 1 else '#' + token

    def camel_case_split(self, line):
        phrases = []
        for word in re.split(r'\s+', line):
            phrases.append(self.hashtag_stringify(word[1:]) if len(word) > 0 and word[0] == '#' else word)
        return ' '.join(phrases)


# Arguments : Path to input file, Path to config file, Path to output file
# e.g. python PreProcessor.py tweets.txt preprocess_config.json cleaned_data.txt
if __name__ == '__main__':
    p = PreProcessor(sys.argv[2])
    p.write_file(sys.argv[3], p.pre_process(sys.argv[1]))
