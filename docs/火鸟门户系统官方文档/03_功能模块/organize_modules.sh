#!/bin/bash

# 功能模块整理脚本
BASE_DIR="/Users/zhiledeng/Desktop/Trea/华人平台官方文档"
MODULE_DIR="$BASE_DIR/03_功能模块"

# 定义模块映射关系 (PDF文件编号:目录名)
declare -A modules=(
    ["05"]="房产门户"
    ["07"]="美食外卖"
    ["08"]="在线商城"
    ["09"]="任务悬赏"
    ["10"]="装修门户"
    ["11"]="投票活动"
    ["12"]="团购秒杀"
    ["13"]="视频频道"
    ["14"]="视频直播"
    ["15"]="贴吧社区"
    ["16"]="互动交友"
    ["17"]="旅游频道"
    ["18"]="教育培训"
    ["19"]="家政服务"
    ["20"]="汽车门户"
    ["21"]="婚嫁频道"
    ["22"]="同城活动"
    ["23"]="养老机构"
    ["24"]="拖拽专题"
    ["25"]="电子报刊"
    ["26"]="自助建站"
    ["27"]="积分商城"
    ["28"]="VR全景"
    ["29"]="图说资讯"
    ["30"]="有奖乐购"
    ["31"]="商品拍卖"
)

# 移动PDF文件到对应目录
for num in "${!modules[@]}"; do
    module_name="${modules[$num]}"
    pdf_file="${num}_${module_name}.pdf"
    
    if [ -f "$MODULE_DIR/$pdf_file" ]; then
        echo "移动 $pdf_file 到 $module_name 目录"
        mv "$MODULE_DIR/$pdf_file" "$MODULE_DIR/$module_name/"
    fi
done

# 为每个模块目录添加必要的基础文档
for module_name in "${modules[@]}"; do
    echo "为 $module_name 添加基础文档"
    
    # 复制系统入门指南
    cp "$BASE_DIR/01_系统管理/系统入门指南.md" "$MODULE_DIR/$module_name/"
    
    # 复制网站后台管理文档
    cp "$BASE_DIR/05_用户指南/网站后台管理.md" "$MODULE_DIR/$module_name/"
    
    # 复制系统API文档
    cp "$BASE_DIR/02_API接口/系统模块API接口文档.md" "$MODULE_DIR/$module_name/"
    
    # 根据模块类型复制相应的API文档
    case $module_name in
        "房产门户"|"汽车门户")
            # 这些模块可能需要信息模块API
            cp "$BASE_DIR/02_API接口/信息模块API接口文档.md" "$MODULE_DIR/$module_name/" 2>/dev/null || true
            ;;
        "招聘求职")
            # 已经处理过了
            ;;
        "美食外卖"|"在线商城"|"积分商城")
            # 这些模块可能需要会员模块API
            cp "$BASE_DIR/02_API接口/会员模块API接口文档.md" "$MODULE_DIR/$module_name/" 2>/dev/null || true
            ;;
        *)
            # 其他模块使用系统API即可
            ;;
    esac
done

echo "模块整理完成！"
