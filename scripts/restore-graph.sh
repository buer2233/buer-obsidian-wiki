#!/bin/bash
# 恢复 Obsidian 图谱颜色配置
# 用法: bash scripts/restore-graph.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VAULT_ROOT="$(dirname "$SCRIPT_DIR")"
GRAPH_FILE="$VAULT_ROOT/.obsidian/graph.json"
BACKUP_FILE="$VAULT_ROOT/.obsidian/graph.json.bak"

if [ ! -f "$BACKUP_FILE" ]; then
  echo "错误: 备份文件不存在: $BACKUP_FILE"
  exit 1
fi

cp "$BACKUP_FILE" "$GRAPH_FILE"
echo "已恢复图谱颜色配置: $GRAPH_FILE"
echo "请重新打开 Obsidian 图谱视图 (Ctrl+G) 查看效果"
