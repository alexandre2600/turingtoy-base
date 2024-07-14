from typing import Dict, List, Optional, Tuple


def run_turing_machine(
    machine: Dict,
    input_: str,
    steps: Optional[int] = None,
) -> Tuple[str, List, bool]:
    memory = list(input_)
    state = machine["start state"]
    position = 0
    reading = memory[position]
    transition = machine["table"][state][reading]
    halted = False
    history = [
        {
            "state": state,
            "reading": memory[position],
            "position": position,
            "memory": "".join(memory),
            "transition": transition,
        }
    ]

    while machine["final states"] and state not in machine["final states"]:
        trace = {}

        # The current state is not in the table
        if state not in machine["table"]:
            halted = True
            memory = list(f"Invalid state: {state}")
            break

        trace["state"] = state

        # Read the current symbol
        try:
            reading = memory[position]
        except IndexError:
            reading = machine["blank"]
            memory.append(reading)

        trace["reading"] = reading

        # The current symbol is not in the table
        if reading not in machine["table"][state]:
            halted = True
            memory = list(f"Invalid symbol: `{reading}` @(p:{position})")
            break

        # Get the transition from the table
        transition = machine["table"][state][reading]

        trace["position"] = position
        trace["memory"] = "".join(memory)
        trace["transition"] = transition

        # Update the state of the Turing machine
        memory, state, position = update_state(
            state, transition, position, memory, machine["blank"]
        )

        # Append the current state of the Turing machine to the history
        history.append(trace)

    memory = clean_memory(memory, machine["blank"])

    return "".join(memory), history, not halted


def clean_memory(memory: List[str], blank: str = " ") -> List[str]:
    while memory and memory[0] == blank:
        memory.pop(0)

    while memory and memory[-1] == blank:
        memory.pop()

    return memory


def update_state(
    state: str,
    transition: Dict | str,
    position: int,
    memory: List[str],
    blank: str = " ",
) -> Tuple[List[str], str, int]:
    # If the transition contains a write operation, update the tape
    if "write" in transition and position < len(memory):
        memory[position] = transition["write"]

    if isinstance(transition, dict):
        position = position + 1 if "R" in transition else position - 1
        state = transition.get("R") if "R" in transition else transition.get("L")

    if isinstance(transition, str):
        position = position + 1 if transition == "R" else position - 1

    if position < 0:
        memory.insert(0, blank)
        position = 0

    return memory, state, position
