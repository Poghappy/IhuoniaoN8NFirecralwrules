#!/bin/bash

# 规范化 API 目录下的文件命名
# 将 # 开头的文件重命名为 kebab-case 格式

set -e

API_DIR="官方资料/API"
cd "$(dirname "$0")/.." || exit 1

echo "开始规范化 API 目录文件命名..."

# 重命名以 # 开头的文件
cd "$API_DIR" || exit 1

# Batch Scrape.yml -> batch-scrape.yml
[ -f "# Batch Scrape.yml" ] && mv "# Batch Scrape.yml" "batch-scrape.yml" && echo "✓ batch-scrape.yml"

# Cancel Batch Scrape.yml -> cancel-batch-scrape.yml
[ -f "# Cancel Batch Scrape.yml" ] && mv "# Cancel Batch Scrape.yml" "cancel-batch-scrape.yml" && echo "✓ cancel-batch-scrape.yml"

# Cancel Crawl.yml -> cancel-crawl.yml
[ -f "# Cancel Crawl.yml" ] && mv "# Cancel Crawl.yml" "cancel-crawl.yml" && echo "✓ cancel-crawl.yml"

# Crawl Params Preview.yml -> crawl-params-preview.yml
[ -f "# Crawl Params Preview.yml" ] && mv "# Crawl Params Preview.yml" "crawl-params-preview.yml" && echo "✓ crawl-params-preview.yml"

# Crawl.yml -> crawl.yml
[ -f "# Crawl.yml" ] && mv "# Crawl.yml" "crawl.yml" && echo "✓ crawl.yml"

# Credit Usage.yml -> credit-usage.yml
[ -f "# Credit Usage.yml" ] && mv "# Credit Usage.yml" "credit-usage.yml" && echo "✓ credit-usage.yml"

# Extract.yml -> extract.yml
[ -f "# Extract.yml" ] && mv "# Extract.yml" "extract.yml" && echo "✓ extract.yml"

# Get Active Crawls.yml -> get-active-crawls.yml
[ -f "# Get Active Crawls.yml" ] && mv "# Get Active Crawls.yml" "get-active-crawls.yml" && echo "✓ get-active-crawls.yml"

# Get Batch Scrape Errors.yml -> get-batch-scrape-errors.yml
[ -f "# Get Batch Scrape Errors.yml" ] && mv "# Get Batch Scrape Errors.yml" "get-batch-scrape-errors.yml" && echo "✓ get-batch-scrape-errors.yml"

# Get Batch Scrape Status.yml -> get-batch-scrape-status.yml
[ -f "# Get Batch Scrape Status.yml" ] && mv "# Get Batch Scrape Status.yml" "get-batch-scrape-status.yml" && echo "✓ get-batch-scrape-status.yml"

# Get Crawl Errors.yml -> get-crawl-errors.yml
[ -f "# Get Crawl Errors.yml" ] && mv "# Get Crawl Errors.yml" "get-crawl-errors.yml" && echo "✓ get-crawl-errors.yml"

# Get Crawl Status.yml -> get-crawl-status.yml
[ -f "# Get Crawl Status.yml" ] && mv "# Get Crawl Status.yml" "get-crawl-status.yml" && echo "✓ get-crawl-status.yml"

# Get Extract Status.yml -> get-extract-status.yml
[ -f "# Get Extract Status.yml" ] && mv "# Get Extract Status.yml" "get-extract-status.yml" && echo "✓ get-extract-status.yml"

# Historical Credit Usage.yml -> historical-credit-usage.yml
[ -f "# Historical Credit Usage.yml" ] && mv "# Historical Credit Usage.yml" "historical-credit-usage.yml" && echo "✓ historical-credit-usage.yml"

# Historical Token Usage.yml -> historical-token-usage.yml
[ -f "# Historical Token Usage.yml" ] && mv "# Historical Token Usage.yml" "historical-token-usage.yml" && echo "✓ historical-token-usage.yml"

# Map.yml -> map.yml
[ -f "# Map.yml" ] && mv "# Map.yml" "map.yml" && echo "✓ map.yml"

# Queue Status.yml -> queue-status.yml
[ -f "# Queue Status.yml" ] && mv "# Queue Status.yml" "queue-status.yml" && echo "✓ queue-status.yml"

# Scrape.yml -> scrape.yml
[ -f "# Scrape.yml" ] && mv "# Scrape.yml" "scrape.yml" && echo "✓ scrape.yml"

# Search.yml -> search.yml
[ -f "# Search.yml" ] && mv "# Search.yml" "search.yml" && echo "✓ search.yml"

# Token Usage -> token-usage.yml (注意这个文件没有 .yml 扩展名)
[ -f "# Token Usage" ] && mv "# Token Usage" "token-usage.yml" && echo "✓ token-usage.yml"

# > Firecrawl API Reference (v2).md -> firecrawl-api-reference-v2.md
[ -f "> Firecrawl API Reference (v2).md" ] && mv "> Firecrawl API Reference (v2).md" "firecrawl-api-reference-v2.md" && echo "✓ firecrawl-api-reference-v2.md"

cd - > /dev/null

echo ""
echo "✅ API 目录文件命名规范化完成！"

