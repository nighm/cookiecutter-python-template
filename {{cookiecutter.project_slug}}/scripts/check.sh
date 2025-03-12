#!/bin/bash

# 运行代码质量检查的快捷脚本

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 默认检查级别
LEVEL=${1:-basic}

# 验证检查级别
case $LEVEL in
    basic|standard|advanced)
        ;;
    *)
        echo "错误: 无效的检查级别 '$LEVEL'"
        echo "可用的级别: basic, standard, advanced"
        exit 1
        ;;
esac

# 运行检查脚本
python "$SCRIPT_DIR/run_quality_checks.py" --level "$LEVEL" 