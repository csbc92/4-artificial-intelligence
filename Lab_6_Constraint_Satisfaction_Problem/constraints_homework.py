from random import shuffle

from pip._vendor.pyparsing import col


class CSP:
    def __init__(self, variables, domains, neighbours, constraints):
        self.variables = variables
        self.domains = domains
        self.neighbours = neighbours
        self.constraints = constraints

    def backtracking_search(self):
        return self.recursive_backtracking({})

    def recursive_backtracking(self, assignment):
        # This method follows the PSEUDO CODE from the book and from exercise.
        if self.is_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)

        for value in self.order_domain_values(var, assignment):
            if self.is_consistent(var, value, assignment):
                assignment.__setitem__(var, value)
                result = self.recursive_backtracking(assignment)
                if result is not None:
                    return result
                assignment.pop(var)

        return None


    def select_unassigned_variable(self, assignment):
        for variable in self.variables:
            if variable not in assignment:
                return variable

    def is_complete(self, assignment):
        for variable in self.variables:
            if variable not in assignment:
                return False
        return True

    def order_domain_values(self, variable, assignment):
        all_values = self.domains[variable][:]
        # shuffle(all_values)
        return all_values

    def is_consistent(self, variable, value, assignment):
        if not assignment:
            return True

        for constraint in self.constraints.values():
            for neighbour in self.neighbours[variable]:
                if neighbour not in assignment:
                    continue

                neighbour_value = assignment[neighbour]
                if not constraint(variable, value, neighbour, neighbour_value):
                    return False
        return True

def create_south_america_csp():

    costa_rica, panama, columbia, ecuador, peru, bolivia, chile, argentina, paraguay, uruguay, brasil, guyane, suriname, guyana, venezuela = \
        "CR", "PA", "C", "E", "P", "BOL", "C", "ARG", "PGY", "UGY", "BR", "GYE", "SUR", "GYA", "VEN"

    values = ['Red', 'Green', 'Blue', 'Yellow']
    variables = [costa_rica, panama, columbia, ecuador, peru, bolivia, chile, argentina, paraguay, uruguay, brasil, guyane, suriname, guyana, venezuela]
    domains = {
        costa_rica: values[:],
        panama: values[:],
        columbia: values[:],
        ecuador: values[:],
        peru: values[:],
        bolivia: values[:],
        chile: values[:],
        argentina: values[:],
        paraguay: values[:],
        uruguay: values[:],
        brasil: values[:],
        guyane: values[:],
        suriname: values[:],
        guyana: values[:],
        venezuela: values[:],
    }
    neighbours = {
        costa_rica: [panama],
        panama: [costa_rica, columbia],
        columbia: [panama, ecuador, peru, brasil, venezuela],
        ecuador: [columbia, peru],
        peru: [ecuador, columbia, brasil, bolivia, chile],
        bolivia: [peru, chile, argentina, paraguay, brasil],
        chile: [argentina, bolivia, peru],
        argentina: [uruguay, brasil, paraguay, bolivia, chile],
        paraguay: [argentina, brasil, bolivia],
        uruguay: [brasil, argentina],
        brasil: [guyana, suriname, guyana, venezuela, columbia, peru, bolivia, paraguay, argentina, uruguay],
        guyane: [brasil, suriname],
        suriname: [brasil, guyane, guyana],
        guyana: [brasil, suriname, venezuela],
        venezuela: [brasil, guyana, columbia],
    }

    def constraint_function(first_variable, first_value, second_variable, second_value):
        return first_value != second_value

    constraints = {
        costa_rica: constraint_function,
        panama: constraint_function,
        columbia: constraint_function,
        ecuador: constraint_function,
        peru: constraint_function,
        bolivia: constraint_function,
        chile: constraint_function,
        argentina: constraint_function,
        paraguay: constraint_function,
        uruguay: constraint_function,
        brasil: constraint_function,
        guyane: constraint_function,
        suriname: constraint_function,
        guyana: constraint_function,
        venezuela: constraint_function,
    }

    return CSP(variables, domains, neighbours, constraints)


if __name__ == '__main__':
    south_america = create_south_america_csp()
    result = south_america.backtracking_search()

    for area, color in sorted(result.items()):
        print("{}: {}".format(area, color))

    # Check at https://mapchart.net/australia.html
