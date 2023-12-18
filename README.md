# pipeline-tester-py

[Menci/pipeline-tester](https://github.com/Menci/pipeline-tester) 的 Python 版  

## 使用方法

### 使用 Vivado 编译仿真  

#### 修改 `run.json`

- compiler: 使用的编译器，应填入 "vivado"
- vivado_path: Vivado Tcl Shell 的批处理文件/bash脚本位置
- mars_run_params: 参照实验指导

### 使用 iverlog 编译仿真  

#### 新建一个 testbench 文件在工程目录下  

1. 注意修改 `TopLevel` 为你的顶层模块名
2. 记住这个文件的路径如 `test_bench_file = dir/mips_tb.v`，其是调用 python 脚本时输入的第三个参数

```iverilog
`timescale 1us/1us
module mips_tb;

reg reset, clock;

// The top level module name should be always "TopLevel"
TopLevel topLevel(.reset(reset), .clock(clock));

integer k;
initial begin
    // posedge clock

    // Hold reset for one cycle
    reset = 1;
    clock = 0; #1;
    clock = 1; #1;
    clock = 0; #1;
    reset = 0; #1;
    
    // This line is commented when testing
    // $stop;

    #1;
    for (k = 0; k < 1000; k = k + 1) begin
        clock = 1; #5;
        clock = 0; #5;
    end

    // Please finish with `syscall`, finishes here may mean the clocks are not enough (really?)
    $finish;
end
    
endmodule
```

#### 如果无法读入 code.txt 与 data.txt  

修改 InstructionMemory 模块读入指令的路径  

`$readmemh("dir/code.txt", memory);`

`dir` 是上一步提到的 `testbench` 文件所在目录

#### 安装 iverilog  

- Windows: [Icarus Verilog for Windows](https://bleyer.org/icarus/)  
- Linux/macOS: 使用包管理器  

#### 修改 `run.json`

- compiler: 使用的编译器，应填入 "iverilog"
- iverilog_path: iverilog 路径
- vvp_path: vvp 路径
- test_bench_only:  
  - `true` 代表你的代码中有合理的 `include` 伪指令，仅需要编译一个 testbench 文件  
  - `false` 代表你的代码中没有 `include` 伪指令，需要将 testbench 文件所在目录下（包括子目录）所有 verilog 代码传入编译器  
- mars_run_params: 参照实验指导

如果你遇到了编译顺序的问题，请合理使用 `include` 伪指令。    

### 运行  

运行测试

```bash
python main.py test test_loop_count test_bench_file
```

仅生成测试

```bash
python main.py gen test_loop_count target_dir
```

运行单个asm文件  

```bash
python main.py run test_bench_file test_asm
```

> `test_loop_count` 是一个整数，代表运行/生成几个测试样例  
> 如果你使用 iverilog 编译，`test_bench_file` 应填入 testbench 文件路径  
> 如果你使用 vivado 编译，`test_bench_file` 应填入 vivado 工程文件 (.xpr) 路径  

### 其他

如果你遇到了下周期的内存写比这周期的寄存器写先输出的问题，可以按如下方式修改 dm 模块输出  

```
reg [31:0] reg_pc;
reg [31:0] reg_addr;
reg [31:0] reg_data;
always @(posedge clock) begin
    if (write_size != 0) begin
        reg_pc = pc;
        reg_addr = {29'(offset), 2'b0};
        reg_data = data_to_write;

        #1 $display("@%h: *%h <= %h", reg_pc, reg_addr, reg_data);
    end
end
```

### verilog 50 inst 测试指南

#### 算法测试

即测试 `mips-asm-test` 内的代码，他们保证不死循环，所以你应该将 `run.json` 中 `mars_run_params` 内的数字调得足够大，比如 50000，`mips_tb.v` 内同理。

由于标程会输出结果，如果你的输出少了这一行，程序会输出一个 Warning，不会认为是错误。


运行指令：`python main.py run test_bench_file /path/to/mips-asm-test`

第二个参数是 `mips_tb.v` 的路径，第三个参数现在可以是目录，表示测试目录下所有 `*.asm`

#### 随机指令测试

因为很容易死循环，所以周期数不要太大，现在仓库已经把所有50条指令打开，见 [p5generator.py](./p5generator.py)

运行指令： `python main.py test test_loop_count test_bench_file`