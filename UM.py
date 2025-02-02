from typing import Self
from Decoder import Decoder

class UniversalMachine():
    def __init__(self: Self) -> None:
        self._inputs: list[int] = []
        self._program_lines: list[int] = []
        
        self._var_env: dict = {}
        self._label_env: dict = {}
        self._bytecodes: list[tuple] = []
        self._snapshots: list = []
        self._max_var: int = 0
        
        self._decoder: Decoder = Decoder()
        self._STATE: dict[int] = {'END': -1, 'JMP':-2, 'NXT': -3}
        
    def input(self: Self) -> None:
        self._program_lines: list[int] = [int(x) for x in input().split()]
        self._inputs: list[int] = [int(x) for x in input().split()]
    
    def vars_init(self: Self) -> None:
        var_list: list[int] = []
        for _, _, var in self._bytecodes:
            var_list.append(var) 
        self._max_var: int = max(var_list) + 1
        counter = 0
        for var in range(self._max_var):
            var_name = self._decoder.var_decoder(var)
            if var % 2 != 0 and (var // 2) < len(self._inputs):
                self._var_env[var_name] = self._inputs[counter]
                counter += 1
                continue
            self._var_env[var_name] = 0
    
    def labels_init(self: Self) -> None:
        for index, (label, _, _) in enumerate(self._bytecodes):
            if not label:
                continue
            label_name = self._decoder.label_decoder(label)
            self._label_env[label_name] = index

    def precompile(self: Self) -> None:
        # Change Code Into Bytecode
        for instruction_code in self._program_lines:
            instruction_bytecode = self._decoder.instruction_to_pair(instruction_code) # (label, cmd, var)
            self._bytecodes.append(instruction_bytecode)
    
    def execute(self: Self, bytecode: tuple[int, int ,int]) -> int:
        label, cmd, var = bytecode
        var_name = self._decoder.var_decoder(var)
        label_name = self._decoder.label_decoder(cmd - 2)
        match cmd:
            case 0:
                pass
                return self._STATE['NXT']
            case 1:
                self._var_env[var_name] += 1
                return self._STATE['NXT']
            case 2:
                self._var_env[var_name] -= 1 if self._var_env[var_name] > 0 else 0 
                return self._STATE['NXT']
            case _:
                if not self._var_env[var_name]:
                    return self._STATE['NXT']
                return self._label_env.get(label_name, self._STATE['END']) # Else self._STATE['JMP']
    
    def take_snapshot(self: Self, line: int) -> None:
        snapshot: str = f'{line} '
        for key in sorted(self._var_env.keys()):
            if key == 'Y':
                continue
            snapshot += f'{self._var_env[key]} '
        snapshot += f'{self._var_env['Y']}'
        self._snapshots.append(snapshot)
    
    def output(self: Self) -> str:
        return '\n'.join(self._snapshots)
    
    def engine(self: Self) -> None:
        self.input()
        
        self.precompile()
        self.labels_init()
        self.vars_init()
        
        program_counter: int = 0
        while program_counter != -1 and program_counter < len(self._bytecodes):
            self.take_snapshot(program_counter + 1)
            instruction_bytecode: tuple[int, int, int] = self._bytecodes[program_counter]
            state: int = self.execute(instruction_bytecode)
            if state == self._STATE['END']:
                break
            elif state == self._STATE['NXT']:
                program_counter += 1
            else:
                program_counter = state
    
if __name__ == '__main__':
    um = UniversalMachine()
    um.engine()
    print(um.output())

