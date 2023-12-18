#! /usr/bin/env python3

import sys
from p5generator import P5Generator
from mars import *
import json

def run_program(code: str, run_config, test_run, tb_file, runner_path):
    def gen_lines(result):
        lines = [s.strip() for s in filter(lambda x: x.__contains__("@") or x.strip().isdigit(), result.split("\n"))]
        for i, line in enumerate(lines):
            if not line.startswith("@") and "@" in line:
                lines.insert(i, line[0 : line.find("@")])
                lines[i + 1] = line[line.find("@") :]
        return lines
    
    with open("test.asm", "w") as fout:
        fout.write(code)

    mars_results = mars_run("test.asm", run_config["mars_run_params"])
    mars_lines = gen_lines(mars_results)
    print(f"Mars result: {len(mars_lines)} lines")
    
    with open('code.txt', 'w') as fout:
        fout.write(mars_compile("test.asm", run_config["im_length"]))

    with open('data.txt', 'w') as fout:
        fout.write('00000000\n' * 2048)

    user_results = test_run(tb_file, runner_path, ['code.txt', 'data.txt'])
    user_lines = gen_lines(user_results)
    print(f"User result: {len(user_lines)} lines")

    with open('user.out', 'w') as fout:
        fout.write("\n".join(user_lines))
    with open('mars.out', 'w') as fout:
        fout.write("\n".join(mars_lines))
    
    return mars_results, user_results, mars_lines, user_lines

def main(args: List[str]):
    if len(args) < 4:
        print(f"Usage: python {args[0]} test test_loop_count test_bench_file")
        print(f"Usage: python {args[0]} gen test_loop_count save_path")
        print(f"Usage: python {args[0]} run test_bench_file asm_file")
        return
            
    with open("run.json") as fin:
        run_config = json.load(fin)
    
    if run_config['compiler'] == 'iverilog':
         from iverilog import test_compile, test_run
         compiler_path = run_config['iverilog_path']
         compiler_config = run_config["iverilog_params"]
         runner_path = run_config['vvp_path']
    elif run_config['compiler'] == 'vivado':
        from vivado import test_compile, test_run
        compiler_path = ''
        compiler_config = ''
        runner_path = run_config['vivado_path']

        print("Using vivado as compiler and simulator. \nPlz ensure that the timestep of test bench is '`timescale 1us/1us'. \nOr the simulation could be slow.\n")
    
    if args[1] == 'test':
        loop_count = int(args[2])
        tb_file = args[3]
        
        test_compile(tb_file, run_config['test_bench_only'], compiler_path, compiler_config)

        for i in range(loop_count):
            print(f"round {i}/{loop_count}")

            mars_results, user_results, mars_lines, user_lines = run_program(P5Generator(True).generate(), run_config, test_run, tb_file, runner_path)

            try:
                if '00002ffc' in user_lines[0]:
                    user_lines = user_lines[1:]
                
                for lino, (user_line, mars_line) in enumerate(zip(user_lines, mars_lines), 1):
                    if user_line.split() != mars_line.split():
                        raise ValueError(f"ERROR at line {lino}\nuser:\n{user_line}\nmars:\n{mars_line}")
            except ValueError as e:
                    print(*e.args, sep='\n')
                    print("You can check file test.asm, code.txt, user.out and mars.out")
                    
                    return
    elif args[1] == 'gen':
        loop_count = int(args[2])
        target_dir = args[3]

        for i in range(loop_count):
            with open(os.path.join(target_dir, f"test_{i}.asm"), "w") as fout:
                fout.write(P5Generator(True).generate())
            
            with open(os.path.join(target_dir, f"code_{i}.txt"), 'w') as fout:
                fout.write(mars_compile(os.path.join(target_dir, f"test_{i}.asm"), run_config["im_length"]))

            with open(os.path.join(target_dir, f"mars_{i}.out"), 'w') as fout:
                fout.write(mars_run(os.path.join(target_dir, f"test_{i}.asm"), run_config["mars_run_params"]))
    elif args[1] == 'run':
        tb_file = args[2]
        asm_file_dir = args[3]
        if os.path.isdir(asm_file_dir):
            asm_dir = asm_file_dir
            test_compile(tb_file, run_config["test_bench_only"], compiler_path, compiler_config)
            for file in os.listdir(asm_dir):
                if not file.endswith(".asm"):
                    continue
                asm_file = os.path.join(asm_dir, file)
                print(f"Running {asm_file}")
                with open(asm_file, encoding="utf-8") as fin:
                    asm_data = fin.read()
                _, _, mars_lines, user_lines = run_program(asm_data, run_config, test_run, tb_file, runner_path)
                try:
                    mars_iter = iter(mars_lines)
                    for lino, (user_line, mars_line) in enumerate(zip(user_lines, mars_iter), 1):
                        if user_line.split() != mars_line.split() and mars_line.isdigit():
                            print(f"Warning: at line {lino}\nuser:\n{user_line}\nmars:\n{mars_line}")
                            mars_line = next(mars_iter)
                        if user_line.split() != mars_line.split():
                            raise ValueError(f"ERROR at line {lino}\nuser:\n{user_line}\nmars:\n{mars_line}")
                    print("{} PASSED".format(asm_file))
                except ValueError as e:
                        print(*e.args, sep='\n')
                        print("You can check file test.asm, code.txt, user.out and mars.out")
                        exit(0)
                print("----------------------------------------------")
        else:
            asm_file = asm_file_dir
            with open(asm_file) as fin:
                asm_data = fin.read()
            test_compile(tb_file, run_config['test_bench_only'], compiler_path, compiler_config)
            _, _, mars_lines, user_lines = run_program(asm_data, run_config, test_run, tb_file, runner_path)
            try:
                mars_iter = iter(mars_lines)
                for lino, (user_line, mars_line) in enumerate(zip(user_lines, mars_iter), 1):
                    if user_line.split() != mars_line.split() and mars_line.isdigit():
                        print(f"Warning: at line {lino}\nuser:\n{user_line}\nmars:\n{mars_line}")
                        mars_line = next(mars_iter)
                    if user_line.split() != mars_line.split():
                        raise ValueError(f"ERROR at line {lino}\nuser:\n{user_line}\nmars:\n{mars_line}")
                print("{} PASSED".format(asm_file))
            except ValueError as e:
                    print(*e.args, sep='\n')
                    print("You can check file test.asm, code.txt, user.out and mars.out")
                    exit(0)

if __name__ == '__main__':
    main(sys.argv)
    # python .\main.py run D:\Code\mips\inst50\mips_tb.v D:\Code\mips\mips-asm-test
