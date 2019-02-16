import argparse

class DFA:
    def __init__(self, states, alphabet, initial_state, final_states, transitions, labels, actions):
        self.states = states
        self.alphabet = alphabet
        self.initial_state = initial_state
        self.final_states = final_states
        self.transitions = transitions
        self.labels = labels
        self.actions = actions

def parse_input_into_dfa(input_file):
    with open(input_file, "r") as file:
        lines = file.readlines()
        states = lines[0].strip().replace(" ", "").split(",")
        alphabet = lines[1].strip().replace(" ", "").split(",")
        initial_state = lines[2].strip()
        final_states = lines[3].strip().replace(" ", "").split(",")

        #parse transitions into an array of dicts
        transitions_before_structuring = [element.split(",") for element in lines[4].strip().replace(" ", "").replace("),(", "SEPARATOR").replace("(", "").replace(")","").split("SEPARATOR")]
        transitions= []

        for transition in transitions_before_structuring:
            transition_dict = dict()
            transition_dict['from_state'] = transition[0]
            transition_dict['condition'] = transition[1]
            transition_dict['to_state'] = transition[2]
            transitions.append(transition_dict)

        #parse labels into a dict
        labels = [element.split(",") for element in lines[5].strip().replace("), (", "),(").replace("),(", "SEPARATOR").replace("(", "").replace(")","").split("SEPARATOR")]
        labels = [[element.strip() for element in label] for label in labels]
        labels_dict = dict()

        for label in labels:
            labels_dict[label[0]] = label[1]

        #parse actions into a dict
        actions = [element.split(",") for element in lines[6].strip().replace(", ", ",").replace("),(", "SEPARATOR").replace("(", "").replace(")", "").split("SEPARATOR")]
        actions = [[element.strip() for element in action] for action in actions]
        actions_dict = dict()

        for action in actions:
            actions_dict[action[0]] = action[1]

    return DFA(states, alphabet, initial_state, final_states, transitions, labels_dict, actions_dict)


def DFA_to_action(dfa, input_string):
    output = ""
    pointer = 0
    last_final_state = -1
    last_final_state_index = -1

    while pointer < len(input_string):
        current_state = dfa.initial_state
        last_valid_state = -1
        last_valid_state_index = -1

        for char_index in range(pointer, len(input_string)):
            for transition in dfa.transitions:
                # print("CHAR", input_string[char_index])
                # print("CONDITION", transition['condition'])
                # print("CURRENT STATE", current_state)
                # print("from_state", transition['from_state'])
                if input_string[char_index] == transition['condition'] and current_state == transition['from_state']:
                    current_state = transition['to_state']

                    if current_state in dfa.final_states:
                        last_valid_state_index = char_index
                        last_valid_state = current_state
                    break
        if not (last_valid_state_index == -1):
            output += input_string[pointer: last_valid_state_index + 1] + ", " + dfa.actions[dfa.labels[last_valid_state]] + "\n"
            pointer = last_valid_state_index + 1
        else:
            output = input_string + ", " + dfa.actions[dfa.labels['DEAD']] + "\n"
            pointer = len(input_string)

    return output



if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True, description='Sample Commandline')

    parser.add_argument('--dfa-file', action="store", help="path of file to take as input to construct DFA", nargs="?", metavar="dfa_file")
    parser.add_argument('--input-file', action="store", help="path of file to take as input to test strings in on DFA", nargs="?", metavar="input_file")
    
    args = parser.parse_args()

    dfa_file = args.dfa_file
    input_file = args.input_file

    dfa = parse_input_into_dfa(dfa_file)

    output_file = open('task_3_1_result.txt', 'w+')

    with open(input_file, "r") as file:
        lines = file.readlines()
        for line in lines:
            output = DFA_to_action(dfa, line.strip())
            print(output)
            output_file.write(output)


