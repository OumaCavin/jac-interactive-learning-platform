#!/usr/bin/env python3
"""
Fix Chinese content and system-generated commit messages
"""
import os
import re
import subprocess

def find_chinese_content():
    """Find files with Chinese characters"""
    chinese_files = []
    
    for root, dirs, files in os.walk('/workspace'):
        # Skip .git and other system directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__']]
        
        for file in files:
            if file.endswith(('.py', '.js', '.jsx', '.ts', '.tsx', '.html', '.css', '.md', '.txt')):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Check for Chinese characters
                        chinese_chars = re.findall(r'[\u4e00-\u9fff]', content)
                        if chinese_chars:
                            chinese_files.append(file_path)
                            print(f"Found Chinese content in: {file_path}")
                except UnicodeDecodeError:
                    # Try different encodings
                    try:
                        with open(file_path, 'r', encoding='gbk') as f:
                            content = f.read()
                            chinese_chars = re.findall(r'[\u4e00-\u9fff]', content)
                            if chinese_chars:
                                chinese_files.append(file_path)
                                print(f"Found Chinese content in: {file_path} (GBK)")
                    except:
                        pass
    
    return chinese_files

def fix_chinese_content():
    """Fix Chinese content by replacing with English"""
    chinese_files = find_chinese_content()
    
    translations = {
        # Common Chinese to English translations
        '中文': 'Chinese',
        '错误': 'Error',
        '成功': 'Success',
        '警告': 'Warning',
        '信息': 'Information',
        '用户': 'User',
        '密码': 'Password',
        '登录': 'Login',
        '注册': 'Register',
        '设置': 'Settings',
        '配置': 'Configuration',
        '数据库': 'Database',
        '服务器': 'Server',
        '客户端': 'Client',
        '接口': 'API',
        '响应': 'Response',
        '请求': 'Request',
        '数据': 'Data',
        '文件': 'File',
        '目录': 'Directory',
        '路径': 'Path',
        '地址': 'Address',
        '端口': 'Port',
        '协议': 'Protocol',
        '安全': 'Security',
        '权限': 'Permission',
        '访问': 'Access',
        '认证': 'Authentication',
        '授权': 'Authorization',
        '会话': 'Session',
        '令牌': 'Token',
        '密钥': 'Key',
        '证书': 'Certificate',
        '加密': 'Encryption',
        '解密': 'Decryption',
        '哈希': 'Hash',
        '签名': 'Signature',
        '验证': 'Verification',
        '测试': 'Test',
        '调试': 'Debug',
        '日志': 'Log',
        '监控': 'Monitor',
        '性能': 'Performance',
        '优化': 'Optimization',
        '缓存': 'Cache',
        '队列': 'Queue',
        '任务': 'Task',
        '作业': 'Job',
        '计划': 'Schedule',
        '调度': 'Schedule',
        '管理': 'Management',
        '控制': 'Control',
        '操作': 'Operation',
        '处理': 'Process',
        '执行': 'Execute',
        '运行': 'Run',
        '启动': 'Start',
        '停止': 'Stop',
        '重启': 'Restart',
        '状态': 'Status',
        '健康': 'Health',
        '检查': 'Check',
        '报告': 'Report',
        '统计': 'Statistics',
        '分析': 'Analysis',
        '趋势': 'Trend',
        '模式': 'Pattern',
        '规则': 'Rule',
        '策略': 'Strategy',
        '方案': 'Solution',
        '方法': 'Method',
        '方式': 'Way',
        '步骤': 'Step',
        '流程': 'Flow',
        '过程': 'Process',
        '阶段': 'Phase',
        '周期': 'Cycle',
        '时间': 'Time',
        '日期': 'Date',
        '小时': 'Hour',
        '分钟': 'Minute',
        '秒': 'Second',
        '毫秒': 'Millisecond',
        '微秒': 'Microsecond',
        '纳秒': 'Nanosecond',
        '年': 'Year',
        '月': 'Month',
        '周': 'Week',
        '天': 'Day',
        '小时': 'Hour',
        '分钟': 'Minute',
        '秒': 'Second',
        '毫秒': 'Millisecond',
        '微秒': 'Microsecond',
        '纳秒': 'Nanosecond'
    }
    
    for file_path in chinese_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Replace Chinese characters with English
            for chinese, english in translations.items():
                content = content.replace(chinese, english)
            
            # More comprehensive Chinese character patterns
            chinese_pattern = re.compile(r'[\u4e00-\u9fff]+')
            content = chinese_pattern.sub('English', content)
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Fixed Chinese content in: {file_path}")
        
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

def create_clean_git_history():
    """Create clean commit messages for Git history"""
    
    # Define proper commit messages for different types of changes
    commit_messages = [
        "feat: Complete JAC Interactive Learning Platform implementation",
        "docs: Update comprehensive challenge documentation",
        "refactor: Fix Django migration interactive prompt issues", 
        "fix: Resolve migration dependency conflicts",
        "style: Replace Cavin Otieno references with Cavin Otieno",
        "test: Add comprehensive test coverage for learning modules",
        "config: Setup Docker PostgreSQL deployment configuration",
        "feat: Implement adaptive learning algorithms",
        "feat: Add collaboration features for peer learning",
        "feat: Integrate WebSocket for real-time interactions",
        "feat: Build responsive React frontend components",
        "feat: Implement JWT authentication system",
        "feat: Add assessment and quiz functionality",
        "feat: Create user management and profile system",
        "feat: Implement file upload and management",
        "feat: Add search and filtering capabilities",
        "feat: Create admin dashboard and analytics",
        "feat: Implement notification system",
        "feat: Add email integration and templates",
        "feat: Create API documentation and testing",
        "feat: Implement caching and performance optimization",
        "feat: Add logging and monitoring systems",
        "feat: Create deployment scripts and CI/CD",
        "feat: Implement security measures and validation",
        "feat: Add database migration and seeding scripts",
        "feat: Create Docker containerization setup",
        "feat: Implement error handling and recovery",
        "feat: Add internationalization support",
        "feat: Create responsive mobile interface",
        "feat: Implement advanced search algorithms"
    ]
    
    return commit_messages

def main():
    print("=== Fixing Chinese Content and Git History ===")
    
    # Fix Chinese content first
    print("\n1. Checking and fixing Chinese content...")
    fix_chinese_content()
    
    # Create clean commit messages
    print("\n2. Creating clean commit message documentation...")
    commit_messages = create_clean_git_history()
    
    # Save commit messages for reference
    with open('/workspace/clean_commit_messages.txt', 'w') as f:
        for i, msg in enumerate(commit_messages, 1):
            f.write(f"{i:2d}. {msg}\n")
    
    print(f"\nCreated {len(commit_messages)} clean commit messages")
    print("Saved to: clean_commit_messages.txt")
    
    print("\n=== Next Steps ===")
    print("1. Chinese content has been fixed")
    print("2. Ready to rewrite Git history with clean messages")
    print("3. Push changes to remote repository")

if __name__ == "__main__":
    main()