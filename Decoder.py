from typing import Self

class Decoder():
    def __init__(self: Self, commands: list = None) -> None:
        self._list_commands: list = []
        if commands:
            self.get_command_list(commands)
        self._CMD_STATE: list[str] = [
            '%s <- %s',
            '%s <- %s + 1',
            '%s <- %s - 1',
            'IF %s != 0 GOTO %s']
    
    def var_decoder(self: Self, num: int) -> str:
        cmd: str = 'YXZ'
        var = cmd[0]
        if num != 0:
            is_temp: bool = (num + 1) % 2
            var = cmd[is_temp + 1] + str(((num + 1) // 2))
        return var
        
    def label_decoder(self: Self, num: int) -> str:
        if not num:
            return ''
        labels: str = 'ABCDE'
        return labels[(num % 5) - 1] + str((num//5) + 1)
    
    def command_decoder(self: Self, cmd: int, var: str) -> str:
        if cmd > 2:
            label: str = self.label_decoder(cmd - 2)
            cmd = -1
            return self._CMD_STATE[cmd] % (var, label)
        return self._CMD_STATE[cmd] % (var, var)
    
    def pair_decoder(self: Self, num: int) -> tuple[int,int]:
        num += 1
        exp: int = 0
        right = left = 0
        while num % 2 == 0:
            num = num // 2
            exp += 1
        left = exp
        if num != 0:
            right = int((num - 1) / 2)
        return left, right
    
    def instruction_to_pair(self: Self, num: int) -> tuple[int, int, int]:
        label, cmd = self.pair_decoder(num)
        cmd, var = self.pair_decoder(cmd)
        return label, cmd, var
    
    def instruction_decoder(self: Self, num: int) -> str:
        # Pairing Section 
        label, cmd, var = self.instruction_to_pair(num)
        
        # Decode Each Component Section
        label: str = self.label_decoder(label)
        var: str = self.var_decoder(var)
        cmd: str = self.command_decoder(cmd, var)
        return f'[{label}] {cmd}\n' if label else f'{cmd}\n'
        
    def decode(self: Self) -> str:
        program: str = ''
        for instruction_code in self._list_commands:
            program += self.instruction_decoder(instruction_code)
        return program
    
    def get_command_list(self: Self, commands: list) -> None:
        self._list_commands: list = commands
 
        
if __name__ == '__main__':
    decoder: Decoder = Decoder([21, 46])
    print(decoder.decode())
    # decoder.get_command_list([0, 1])
    # print(decoder.decode())