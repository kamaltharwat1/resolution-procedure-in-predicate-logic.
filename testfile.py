import re
def eliminate_implication(sentence):
    while 'Implies' in sentence:
        pos = sentence.find('Implies')
        left = sentence[:pos].strip()
        right = sentence[pos + 2:].strip()
        sentence = '(' + 'Not' + left + ') or (' + right + ')'
    return sentence

def apply_demorgan(clause):
    if 'and' in clause:
        parts = clause.split('and')
        clause = '(Not' + parts[0].strip() + ' or (Not' + parts[1].strip() + ')'

    elif 'or' in clause:
        parts = clause.split('or')
        clause = '(Not' + parts[0].strip() + ' and (Not' + parts[1].strip() + ')'
    return clause

def get_inner_part(index, clause):
    stack = ['(']
    new_clause = ""
    while len(stack) != 0:
        if clause[index] == '(':
            stack.append('(')
        elif clause[index] == ')':
            stack.pop()
        new_clause += clause[index]
        index += 1
    return new_clause, index

def move_negation_inward(sentence):
    if "Not(" in sentence:
        negation_index = sentence.index("Not(")
        inner_part, closing_index = get_inner_part(negation_index + 2, sentence)
        inner_part = apply_demorgan(inner_part)
        inner_part = move_negation_inward(inner_part)  
        return sentence[:negation_index] + inner_part + sentence[closing_index + 1:]
    return sentence

def remove_double_negations(sentence):
    while "Not Not" in sentence:
        sentence = sentence.replace("Not Not", "")
    return sentence

def standardize_variable_scope(sentence):
    variables = set(sentence.split())
    replacements = {}
    for var in variables:
        replacements[var] = var + '1'
    for var, new_var in replacements.items():
        sentence = sentence.replace(var, new_var)
    return sentence

def prenex_form(sentence):
    quantifiers = []
    while 'Exists' in sentence or 'Forall' in sentence:
        for i, char in enumerate(sentence):
            if char in ['e', 'f']:
                if sentence[i:i+6] == 'Exists':
                    quantifiers.append('Exists')
                elif sentence[i:i+6] == 'Forall':
                    quantifiers.append('Forall')
                break
        sentence = sentence.replace(quantifiers[-1], '', 1)
    return ' '.join(quantifiers) + sentence
def skolemize(expression):
    # matching universal quantifiers
    universal_pattern = r'∀\s*([a-zA-Z]+)\s*'

    # matching existential quantifiers
    existential_pattern = r'∃\s*([a-zA-Z]+)\s*'

    # Find all universal quantifiers
    universal_matches = re.findall(universal_pattern, expression)

    # Find all existential quantifiers
    existential_matches = re.findall(existential_pattern, expression)

    # If no universal quantifier before existance quantifier
    if not universal_matches:
        skolemized_expression = expression
        for variable in existential_matches:
            skolemized_expression = skolemized_expression.replace(f'∃{variable}', '')
            skolemized_expression = skolemized_expression.replace(f'{variable}', 'B')
    else:
        # If a universal quantifier precedes the existential quantifier
        for variable in existential_matches:
            skolemized_expression = re.sub(existential_pattern, f'F({universal_matches[0]})', expression)

    return skolemized_expression

# Test the function with the provided examples
expressions = [
    "∀x ∃y P(A) ∨ Q(y)",
    "∀x ∃y P(x) ∨ Q(y)"
]

for expression in expressions:
    print("Original Expression:", expression)
    skolemized_expression = skolemize(expression)
    print("Skolemized Expression:", skolemized_expression)
    print()


def eliminate_universal_quantifiers(sentence):
    return sentence.replace('Forall ', '')

def convert_to_cnf(clauses):
    transformed_clauses = []
    for clause in clauses:
        clause = eliminate_implication(clause)
        clause = move_negation_inward(clause)
        clause = remove_double_negations(clause)
        clause =standardize_variable_scope(clause)
        clause =prenex_form(clause)
        clause = eliminate_universal_quantifiers(clause)
        transformed_clauses.append(clause)
    return transformed_clauses
def turn_conjunctions_into_clauses(sentence):
    clauses = sentence.split('and')
    return set(clauses)

def rename_variables_in_clauses(clauses):
    renamed_clauses = []
    for clause in clauses:
        variables = set(clause.split())
        replacements = {}
        for var in variables:
            replacements[var] = var + '1'
        for var, new_var in replacements.items():
            clause = clause.replace(var, new_var)
        renamed_clauses.append(clause)
    return renamed_clauses

def check_consistency(clauses):
    transformed_clauses = convert_to_cnf(clauses)
    for clause in transformed_clauses:
        if "Exists" in clause:
            return False, transformed_clauses
    return True, transformed_clauses

def main():
    
    input_string = input("Enter three strings separated by commas: ").strip()
    strings = input_string.split(',')
    # Test consistency
    consistent, _ = check_consistency(strings)
    if consistent:
        print("The strings are consistent.")
    else:
        print("The strings are inconsistent.")

if __name__ == "__main__":
    main()
