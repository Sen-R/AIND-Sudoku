
from utils import *
from itertools import combinations

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units

# TODO: Update the unit list to add the new diagonal units
diagonal_unit = [r+c for r,c in zip(rows, cols)]
antidiagonal_unit = [r+c for r,c in zip(rows, reversed(cols))]
unitlist = unitlist + [diagonal_unit, antidiagonal_unit]

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).
    """

    
    # TODO: Implement this function!
    # NB in order to make sure I satisfy the test requirements set out above, I'll
    # do this in two passes -- first identifying all naked twins in the input and
    # then processing them in the second pass.
    
    # First identify all naked twins in input
    naked_twin_list = []
    for unit_idx, unit in enumerate(unitlist):
        for combo in combinations(unit, 2):
            lref, lval = combo[0], values[combo[0]]
            rref, rval = combo[1], values[combo[1]]
            if len(lval)==2 and lval == rval:
                # Naked twin
                naked_twin_list.append((unit_idx, lref, rref, lval))

    # Now process naked twins
    for unit_idx, lref, rref, lval in naked_twin_list:
        for ref in unitlist[unit_idx]:
            if ref!=lref and ref!=rref:
                values[ref] = values[ref].replace(lval[0],'')
                values[ref] = values[ref].replace(lval[1],'')

    return values


def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    # TODO: Copy your code from the classroom to complete this function
    solved_cells = {k:v for k,v in values.items() if len(v)==1}
    
    for sc_ref, sc_val in solved_cells.items():
        for peer_ref in peers[sc_ref]:
            values[peer_ref] = values[peer_ref].replace(sc_val,'')
            
    return values


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    # TODO: Copy your code from the classroom to complete this function
    for unit in unitlist:
        for num in "123456789":
            num_in_refs = [ref for ref in unit if num in values[ref]]
            if len(num_in_refs)==1:
                values[num_in_refs[0]] = num
    
    return values    


def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable 
    """
    # TODO: Copy your code from the classroom and modify it to complete this function
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """
    # TODO: Copy your code from the classroom to complete this function
    # First, reduce the puzzle
    values = reduce_puzzle(values)
    if values==False:
        return False # puzzle unsolvable

    # Choose one of the unfilled squares with the fewest possibilities and
    # recurse
    unsolved_box_lengths = [(len(v),k) for k,v in values.items() if len(v)>1]
    if len(unsolved_box_lengths)>0: # puzzle not yet solved
        _,branch_box = min(unsolved_box_lengths)
        branch_vals = values[branch_box]
        for trial_val in branch_vals:
            new_values = dict(values) # get copy
            new_values[branch_box] = trial_val
            new_values = search(new_values)
            if new_values:
                return new_values
        else: # run out of options, so puzzle is unsolvable
            return False
    else: # puzzle solved!
        return values


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
