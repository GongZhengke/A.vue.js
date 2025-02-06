from flask import Blueprint, jsonify, request, session
import requests
from bs4 import BeautifulSoup
import time
import logging
import re
from datetime import datetime, timezone, timedelta

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__)

BASE_URL = 'https://assbbs.com'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

def make_request(method, url, data=None, headers=None, use_auth=True):
    """统一的请求处理函数"""
    try:
        request_headers = HEADERS.copy()
        if headers:
            request_headers.update(headers)
            
        # 如果需要认证且存在认证cookie，则添加到请求中
        cookies = session.get('auth_cookies', {}) if use_auth else None
        
        response = requests.request(
            method,
            url,
            data=data,
            headers=request_headers,
            cookies=cookies,
            timeout=10,
            allow_redirects=False
        )
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"请求失败: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"请求出错: {str(e)}")
        return None

def get_soup(url, use_auth=True):
    """获取页面内容并解析，支持认证"""
    try:
        logger.info(f"正在请求URL: {url}")
        response = make_request('GET', url, use_auth=use_auth)
        if not response:
            return None
            
        logger.debug(f"请求成功，状态码: {response.status_code}")
        return BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        logger.error(f"解析失败: {str(e)}")
        return None

def validate_email(email):
    """验证邮箱格式"""
    pattern = r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def format_time(timestamp):
    """格式化时间显示
    Args:
        timestamp: 时间戳（秒）
    Returns:
        str: 格式化后的时间字符串
    """
    try:
        # 转换时间戳为datetime对象
        dt = datetime.fromtimestamp(int(timestamp), timezone.utc)
        now = datetime.now(timezone.utc)
        
        # 计算时间差
        diff = now - dt
        
        # 计算具体时间差
        seconds = diff.total_seconds()
        
        if seconds < 60:
            return f"{int(seconds)}秒前"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            return f"{minutes}分钟前"
        elif seconds < 86400:  # 24小时内
            hours = int(seconds / 3600)
            return f"{hours}小时前"
        elif seconds < 259200:  # 3天内
            days = int(seconds / 86400)
            return f"{days}天前"
        else:
            # 转换为本地时间
            local_dt = dt.astimezone()
            return local_dt.strftime("%m/%d %H:%M")
    except Exception as e:
        logger.error(f"时间格式化失败: {str(e)}")
        return ""

@api_bp.route('/auth/login', methods=['POST'])
def login():
    """用户登录"""
    try:
        data = request.form
        email = data.get('user')
        password = data.get('pass')  # 已经是MD5加密后的密码
        
        if not email or not password:
            return jsonify({'error': '邮箱或密码不能为空'}), 400
            
        if not validate_email(email):
            return jsonify({'error': '邮箱格式错误'}), 400
            
        # 构建登录请求
        login_data = {
            'user': email,
            'pass': password
        }
        
        # 发送登录请求
        response = make_request(
            'POST',
            f"{BASE_URL}/login",
            data=login_data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            use_auth=False  # 登录时不需要使用已有的cookie
        )
        
        if not response:
            return jsonify({'error': '登录请求失败'}), 500
            
        if response.status_code in [200, 302]:
            # 保存登录状态
            session['user_email'] = email
            # 获取并保存cookies
            cookies = response.cookies.get_dict()
            session['auth_cookies'] = cookies
            
            return jsonify({
                'message': '登录成功',
                'email': email
            }), 200
        else:
            return jsonify({'error': '登录失败'}), 401
            
    except Exception as e:
        logger.error(f"登录时发生错误: {str(e)}")
        return jsonify({'error': f'登录失败: {str(e)}'}), 500

@api_bp.route('/auth/register', methods=['POST'])
def register():
    """用户注册"""
    try:
        data = request.form
        email = data.get('user')
        password = data.get('pass')  # 已经是MD5加密后的密码
        
        if not email or not password:
            return jsonify({'error': '邮箱或密码不能为空'}), 400
            
        if not validate_email(email):
            return jsonify({'error': '邮箱格式错误'}), 400
            
        # 构建注册请求
        register_data = {
            'user': email,
            'pass': password
        }
        
        # 发送注册请求
        response = make_request(
            'POST',
            f"{BASE_URL}/register",
            data=register_data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            use_auth=False  # 注册时不需要使用已有的cookie
        )
        
        if not response:
            return jsonify({'error': '注册请求失败'}), 500
            
        if response.status_code in [200, 302]:
            # 保存登录状态
            session['user_email'] = email
            # 获取并保存cookies
            cookies = response.cookies.get_dict()
            session['auth_cookies'] = cookies
            
            return jsonify({
                'message': '注册成功',
                'email': email
            }), 200
        else:
            return jsonify({'error': '注册失败，邮箱可能已存在'}), 400
            
    except Exception as e:
        logger.error(f"注册时发生错误: {str(e)}")
        return jsonify({'error': f'注册失败: {str(e)}'}), 500

@api_bp.route('/auth/logout', methods=['POST'])
def logout():
    """用户登出"""
    try:
        # 发送登出请求
        response = make_request(
            'POST',
            f"{BASE_URL}/logout",
            use_auth=True  # 登出时需要使用认证cookie
        )
        
        # 清除session
        session.pop('user_email', None)
        session.pop('auth_cookies', None)
        
        if response and response.status_code in [200, 302]:
            return jsonify({'message': '登出成功'}), 200
        else:
            return jsonify({'error': '登出失败'}), 400
            
    except Exception as e:
        logger.error(f"登出时发生错误: {str(e)}")
        return jsonify({'error': f'登出失败: {str(e)}'}), 500

@api_bp.route('/posts')
def get_posts():
    """获取帖子列表"""
    try:
        # 获取时间戳参数（用于分页）
        timestamp = request.args.get('timestamp')
        
        # 构建URL
        if timestamp:
            url = f"{BASE_URL}/l/{timestamp}"  # 使用/l/时间戳格式
        else:
            url = f"{BASE_URL}/"  # 首页
        
        logger.info(f"开始获取帖子列表，URL: {url}")
        soup = get_soup(url)
        if not soup:
            logger.error("获取页面内容失败")
            return jsonify({'error': '获取数据失败'}), 500
        
        posts = []
        # 查找帖子列表容器
        post_list = soup.find('div', class_='post-list')
        if not post_list:
            logger.error("未找到帖子列表容器")
            return jsonify({'error': '未找到帖子列表'}), 500
        
        # 遍历所有帖子
        for post_item in post_list.find_all('a', class_='post-item'):
            try:
                # 获取帖子信息
                post_info = post_item.find('div', class_='post-info')
                post_meta = post_item.find('div', class_='post-meta')
                
                if not post_info or not post_meta:
                    continue
                
                # 解析帖子元数据
                title = post_info.get_text(strip=True)
                href = post_item.get('href', '')
                
                # 获取作者和时间信息
                author_spans = post_meta.find_all('span', class_='author')
                date_spans = post_meta.find_all('span', class_='date')
                replies_span = post_meta.find('span', class_='replies')
                
                create_timestamp = date_spans[0].get('time_stamp') if date_spans else None
                post_data = {
                    'title': title,
                    'url': f"{BASE_URL}{href}",
                    'post_id': href.split('/')[-1],
                    'author': author_spans[0].get_text(strip=True) if author_spans else None,
                    'create_time': {
                        'timestamp': create_timestamp,
                        'formatted': format_time(create_timestamp) if create_timestamp else None
                    }
                }
                
                # 如果有回复信息
                if len(author_spans) > 1 and len(date_spans) > 1 and replies_span:
                    reply_timestamp = date_spans[-1].get('time_stamp')
                    post_data.update({
                        'replies_count': replies_span.get_text(strip=True).replace('❮', '').strip(),
                        'last_reply': {
                            'author': author_spans[-1].get_text(strip=True),
                            'timestamp': reply_timestamp,
                            'formatted': format_time(reply_timestamp) if reply_timestamp else None
                        }
                    })
                
                posts.append(post_data)
                logger.debug(f"成功解析帖子: {title}")
            except Exception as e:
                logger.error(f"解析帖子时出错: {str(e)}")
                continue
        
        # 获取最后一个帖子的最后回复时间作为下一页的时间戳
        next_timestamp = None
        if posts:
            last_post = posts[-1]
            if 'last_reply' in last_post:
                next_timestamp = last_post['last_reply']['timestamp']
            else:
                next_timestamp = last_post['create_time']['timestamp']
        
        logger.info(f"成功获取 {len(posts)} 个帖子")
        return jsonify({
            'total': len(posts),
            'posts': posts,
            'pagination': {
                'next_timestamp': next_timestamp
            }
        })
    except Exception as e:
        logger.error(f"获取帖子列表时发生错误: {str(e)}")
        return jsonify({'error': f'获取数据失败: {str(e)}'}), 500

@api_bp.route('/posts/<post_id>')
def get_post_detail(post_id):
    """获取帖子详情"""
    try:
        # 获取时间戳参数（用于分页）
        timestamp = request.args.get('timestamp')
        
        # 构建URL
        if timestamp:
            url = f"{BASE_URL}/t/{post_id}/m/{timestamp}"
        else:
            url = f"{BASE_URL}/t/{post_id}"
        
        logger.info(f"开始获取帖子详情: {url}")
        
        soup = get_soup(url)
        if not soup:
            logger.error("获取帖子详情页面失败")
            return jsonify({'error': '获取数据失败'}), 500
        
        try:
            # 查找帖子列表容器
            post_list = soup.find('div', class_='post-list')
            if not post_list:
                logger.error("未找到帖子内容")
                return jsonify({'error': '未找到帖子内容'}), 500
            
            posts = []
            # 遍历所有回复
            for post_item in post_list.find_all('div', class_='post-item'):
                try:
                    post_info = post_item.find('div', class_='post-info')
                    post_meta = post_item.find('div', class_='post-meta')
                    
                    if not post_info or not post_meta:
                        continue
                    
                    # 获取回复ID
                    reply_id = post_item.get('id', '').replace('p', '')
                    
                    # 获取引用内容
                    quote = None
                    quote_block = post_info.find('blockquote', class_='blockquote')
                    if quote_block:
                        quote = quote_block.get_text(strip=True)
                    
                    # 获取正文内容（排除引用部分）
                    content_paragraphs = []
                    for p in post_info.find_all('p'):
                        if not p.find_parent('blockquote'):
                            content_paragraphs.append(p.get_text(strip=True))
                    content = '\n'.join(content_paragraphs)
                    
                    # 获取作者信息
                    author_link = post_meta.find('a', class_='author')
                    author = {
                        'name': author_link.get_text(strip=True),
                        'uid': author_link.get('href', '').split('uid=')[-1] if 'uid=' in author_link.get('href', '') else None
                    }
                    
                    # 获取时间信息
                    date_span = post_meta.find('span', class_='date')
                    timestamp = date_span.get('time_stamp') if date_span else None
                    
                    # 获取操作按钮
                    actions = []
                    for action_link in post_meta.find_all('a', class_=['reply', 'edit']):
                        action_type = action_link.get('class')[0]
                        action_url = action_link.get('href', '')
                        if action_url and not action_url.startswith('javascript:'):
                            actions.append({
                                'type': action_type,
                                'url': f"{BASE_URL}{action_url}" if action_url.startswith('/') else action_url
                            })
                    
                    post_data = {
                        'id': reply_id,
                        'content': content,
                        'quote': quote,
                        'author': author,
                        'time': {
                            'timestamp': timestamp,
                            'formatted': format_time(timestamp) if timestamp else None
                        },
                        'actions': actions
                    }
                    
                    posts.append(post_data)
                    logger.debug(f"成功解析回复: {reply_id}")
                except Exception as e:
                    logger.error(f"解析回复时出错: {str(e)}")
                    continue
            
            # 获取分页信息
            pagination = soup.find('div', class_='pagination')
            next_page = None
            prev_page = None
            if pagination:
                next_link = pagination.find('a', string='下页')
                prev_link = pagination.find('a', string='上页')
                if next_link:
                    next_page = next_link.get('href', '').split('/')[-1]
                if prev_link:
                    prev_page = prev_link.get('href', '').split('/')[-1]
            
            logger.info(f"成功获取帖子详情，共 {len(posts)} 条回复")
            return jsonify({
                'id': post_id,
                'posts': posts,
                'pagination': {
                    'next_timestamp': next_page,
                    'prev_timestamp': prev_page
                }
            })
        except Exception as e:
            logger.error(f"解析帖子详情时出错: {str(e)}")
            return jsonify({
                'id': post_id,
                'error': str(e),
                'url': url
            })
            
    except Exception as e:
        logger.error(f"获取帖子详情时发生错误: {str(e)}")
        return jsonify({'error': f'解析数据失败: {str(e)}'}), 500

@api_bp.before_request
def before_request():
    """请求前处理：添加延迟避免请求过快"""
    time.sleep(0.3)  # 添加1秒延迟

@api_bp.route('/auth/status')
def auth_status():
    """获取当前用户登录状态"""
    return jsonify({
        'logged_in': 'user_email' in session,
        'email': session.get('user_email')
    })
