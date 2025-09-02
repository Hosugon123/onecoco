from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import User
from sales.models import Sale
from costs.models import Cost
from reports.models import Report

def home(request):
    """首頁視圖"""
    context = {
        'title': '一口口麻辣串記帳系統',
        'welcome_message': '歡迎使用麻辣燙店記帳系統！',
        'features': [
            '💰 每日銷售額記錄',
            '📊 成本管理和分析',
            '📈 利潤結算和報表',
            '👥 多角色權限管理',
            '🎯 自定義使用者管理後台'
        ]
    }
    return render(request, 'home.html', context)

def about(request):
    """關於頁面"""
    return HttpResponse("""
    <h1>一口口麻辣串記帳系統</h1>
    <p>這是一個專為麻辣燙店設計的記帳和利潤結算系統。</p>
    <p>功能包括：</p>
    <ul>
        <li>銷售額記錄</li>
        <li>成本管理</li>
        <li>利潤分析</li>
        <li>報表生成</li>
    </ul>
    <p><a href="/dashboard/">進入管理後台</a></p>
    """)

def custom_login(request):
    """自定義登入頁面"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'歡迎回來，{user.username}！')
            return redirect('dashboard')
        else:
            messages.error(request, '使用者名稱或密碼錯誤！')
    
    return render(request, 'auth/login.html')

def custom_register(request):
    """自定義註冊頁面"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        role = request.POST.get('role', 'founder')
        
        # 驗證密碼
        if password1 != password2:
            messages.error(request, '兩次輸入的密碼不一致！')
            return render(request, 'auth/register.html')
        
        # 檢查使用者名稱是否已存在
        if User.objects.filter(username=username).exists():
            messages.error(request, '使用者名稱已存在！')
            return render(request, 'auth/register.html')
        
        # 建立新使用者
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                role=role,
                is_staff=True,
                is_superuser=True
            )
            messages.success(request, f'帳號 {username} 建立成功！請使用新帳號登入。')
            return redirect('custom_login')
        except Exception as e:
            messages.error(request, f'建立帳號失敗：{str(e)}')
    
    return render(request, 'auth/register.html')

def custom_logout(request):
    """登出"""
    logout(request)
    messages.success(request, '您已成功登出！')
    return redirect('home')

@login_required
def dashboard(request):
    """使用者管理儀表板"""
    context = {
        'user': request.user,
        'total_users': User.objects.count(),
        'total_sales': Sale.objects.count() if hasattr(Sale, 'objects') else 0,
        'total_costs': Cost.objects.count() if hasattr(Cost, 'objects') else 0,
        'recent_users': User.objects.order_by('-date_joined')[:5],
    }
    return render(request, 'dashboard/index_unified.html', context)

@login_required
def user_management(request):
    """使用者管理頁面"""
    users = User.objects.all().order_by('-date_joined')
    context = {
        'users': users,
        'user': request.user,
    }
    return render(request, 'dashboard/user_management_unified.html', context)

@login_required
def user_detail(request, user_id):
    """使用者詳細資料"""
    user_detail = get_object_or_404(User, id=user_id)
    context = {
        'user_detail': user_detail,
        'user': request.user,
    }
    return render(request, 'dashboard/user_detail.html', context)

@login_required
def user_edit(request, user_id):
    """編輯使用者"""
    user_to_edit = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        # 更新使用者資料
        user_to_edit.first_name = request.POST.get('first_name', '')
        user_to_edit.last_name = request.POST.get('last_name', '')
        user_to_edit.email = request.POST.get('email', '')
        user_to_edit.role = request.POST.get('role', 'founder')
        user_to_edit.is_active = request.POST.get('is_active') == 'on'
        user_to_edit.save()
        
        messages.success(request, f'使用者 {user_to_edit.username} 更新成功！')
        return redirect('user_management')
    
    context = {
        'user_to_edit': user_to_edit,
        'user': request.user,
        'role_choices': User.ROLE_CHOICES,
    }
    return render(request, 'dashboard/user_edit.html', context)

@login_required
def user_delete(request, user_id):
    """刪除使用者"""
    if request.method == 'POST':
        user_to_delete = get_object_or_404(User, id=user_id)
        username = user_to_delete.username
        
        # 防止刪除自己
        if user_to_delete == request.user:
            messages.error(request, '不能刪除自己的帳號！')
        else:
            user_to_delete.delete()
            messages.success(request, f'使用者 {username} 已刪除！')
        
        return redirect('user_management')
    
    return redirect('user_management')

@login_required
def sales_management(request):
    """銷售管理頁面"""
    from sales.models import Sale
    from django.db.models import Sum
    from datetime import date, datetime, timedelta
    from django.utils import timezone
    import calendar
    
    # 獲取篩選參數
    selected_year = request.GET.get('year', timezone.now().year)
    selected_month = request.GET.get('month', timezone.now().month)
    
    try:
        selected_year = int(selected_year)
        selected_month = int(selected_month)
    except (ValueError, TypeError):
        selected_year = timezone.now().year
        selected_month = timezone.now().month
    
    # 計算選定月份的第一天和最後一天
    first_day = date(selected_year, selected_month, 1)
    last_day = date(selected_year, selected_month, calendar.monthrange(selected_year, selected_month)[1])
    
    # 轉換為 datetime 物件以避免 SQLite 的 user-defined function 問題
    start_datetime = timezone.make_aware(datetime.combine(first_day, datetime.min.time()))
    end_datetime = timezone.make_aware(datetime.combine(last_day, datetime.max.time()))
    
    # 獲取今日銷售統計數據
    today = timezone.now().date()
    tomorrow = today + timedelta(days=1)
    today_start = timezone.make_aware(datetime.combine(today, datetime.min.time()))
    today_end = timezone.make_aware(datetime.combine(tomorrow, datetime.min.time()))
    
    # 使用 datetime 範圍查詢
    try:
        today_sales = Sale.objects.filter(
            date__gte=today_start,
            date__lt=today_end
        )
    except Exception as e:
        today_sales = Sale.objects.none()
    
    # 獲取篩選月份的營業額和支出記錄
    try:
        from expenses.models import Expense
        filtered_sales = Sale.objects.filter(
            date__gte=start_datetime,
            date__lte=end_datetime
        ).select_related('recorded_by').order_by('-date')
        
        filtered_expenses = Expense.objects.filter(
            date__gte=start_datetime,
            date__lte=end_datetime
        ).select_related('recorded_by').order_by('-date')
        
        # 計算篩選月份的總計
        sales_total = filtered_sales.aggregate(total=Sum('amount'))['total'] or 0
        expenses_total = filtered_expenses.aggregate(total=Sum('amount'))['total'] or 0
        
    except Exception:
        filtered_sales = Sale.objects.none()
        filtered_expenses = []
        sales_total = 0
        expenses_total = 0
    
    # 生成年份和月份選項
    current_year = timezone.now().year
    years = list(range(current_year - 2, current_year + 2))
    months = [
        (1, '一月'), (2, '二月'), (3, '三月'), (4, '四月'),
        (5, '五月'), (6, '六月'), (7, '七月'), (8, '八月'),
        (9, '九月'), (10, '十月'), (11, '十一月'), (12, '十二月')
    ]
    
    context = {
        'user': request.user,
        'filtered_sales': filtered_sales,
        'filtered_expenses': filtered_expenses,
        'today_sales': today_sales,
        'today_total': today_sales.aggregate(total=Sum('amount'))['total'] or 0,
        'sales_total': sales_total,
        'expenses_total': expenses_total,
        'selected_year': selected_year,
        'selected_month': selected_month,
        'years': years,
        'months': months,
        'current_month_name': dict(months)[selected_month],
    }
    
    return render(request, 'dashboard/sales_management_unified.html', context)

@login_required
def cost_management(request):
    """成本管理頁面"""
    from costs.models import Cost
    
    # 獲取所有成本記錄，按日期倒序排列
    costs = Cost.objects.select_related('recorded_by').order_by('-date', '-created_at')
    
    context = {
        'user': request.user,
        'costs': costs,  # 更新變數名稱以匹配模板
    }
    return render(request, 'dashboard/cost_management_unified.html', context)

@login_required
def delete_cost(request, cost_id):
    """刪除成本項目"""
    from costs.models import Cost
    from django.contrib import messages
    
    try:
        cost = Cost.objects.get(id=cost_id, recorded_by=request.user)
        cost_description = cost.description
        cost.delete()
        messages.success(request, f'成本項目「{cost_description}」已成功刪除！')
    except Cost.DoesNotExist:
        messages.error(request, '找不到要刪除的成本項目，或您沒有權限刪除此項目。')
    except Exception as e:
        messages.error(request, f'刪除失敗：{str(e)}')
    
    return redirect('cost_management')

@login_required
def delete_sale(request, sale_id):
    """刪除銷售記錄"""
    from sales.models import Sale
    from django.contrib import messages
    
    try:
        sale = Sale.objects.get(id=sale_id, recorded_by=request.user)
        sale_description = sale.description or "營業額"
        sale.delete()
        messages.success(request, f'銷售記錄「{sale_description}」已成功刪除！')
    except Sale.DoesNotExist:
        messages.error(request, '找不到要刪除的銷售記錄，或您沒有權限刪除此記錄。')
    except Exception as e:
        messages.error(request, f'刪除失敗：{str(e)}')
    
    return redirect('sales_management')

@login_required
def delete_expense(request, expense_id):
    """刪除支出記錄"""
    from expenses.models import Expense
    from django.contrib import messages
    
    try:
        expense = Expense.objects.get(id=expense_id, recorded_by=request.user)
        expense_description = expense.item_name
        expense.delete()
        messages.success(request, f'支出記錄「{expense_description}」已成功刪除！')
    except Expense.DoesNotExist:
        messages.error(request, '找不到要刪除的支出記錄，或您沒有權限刪除此記錄。')
    except Exception as e:
        messages.error(request, f'刪除失敗：{str(e)}')
    
    return redirect('sales_management')

@login_required
def profit_analysis(request):
    """利潤分析頁面"""
    from sales.models import Sale
    from costs.models import Cost
    from expenses.models import Expense
    from django.db.models import Sum
    from datetime import datetime, timedelta
    from django.utils import timezone
    
    # 獲取本月數據
    today = timezone.now().date()
    first_day = today.replace(day=1)
    # 計算下個月的第一天，然後減去一天得到本月最後一天
    if first_day.month == 12:
        next_month = first_day.replace(year=first_day.year + 1, month=1)
    else:
        next_month = first_day.replace(month=first_day.month + 1)
    last_day = next_month - timedelta(days=1)
    
    # 轉換為 datetime 物件以避免 SQLite 的 user-defined function 問題
    start_datetime = timezone.make_aware(datetime.combine(first_day, datetime.min.time()))
    end_datetime = timezone.make_aware(datetime.combine(last_day, datetime.max.time()))
    
    # 使用 datetime 範圍查詢
    monthly_sales = Sale.objects.filter(
        date__gte=start_datetime,
        date__lte=end_datetime
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    try:
        monthly_expenses = Expense.objects.filter(
            date__gte=start_datetime,
            date__lte=end_datetime
        ).aggregate(total=Sum('amount'))['total'] or 0
    except Exception:
        monthly_expenses = 0
    
    monthly_costs = Cost.objects.filter(
        date__gte=start_datetime,
        date__lte=end_datetime
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # 總支出 = 日常支出 + 固定成本
    total_expenses = monthly_expenses + monthly_costs
    monthly_profit = monthly_sales - total_expenses
    
    context = {
        'user': request.user,
        'monthly_sales': monthly_sales,
        'monthly_expenses': monthly_expenses,
        'monthly_costs': monthly_costs,
        'total_expenses': total_expenses,
        'monthly_profit': monthly_profit,
        'current_month': today.strftime('%Y年%m月'),
    }
    return render(request, 'dashboard/profit_analysis_unified.html', context)

@login_required
def add_cost(request):
    """新增成本項目"""
    if request.method == 'POST':
        from costs.models import Cost
        
        try:
            # 獲取表單數據
            item_name = request.POST.get('item_name')
            unit = request.POST.get('unit', '')
            amount = request.POST.get('amount')
            selling_price = request.POST.get('selling_price')
            category = request.POST.get('category', '食材')
            notes = request.POST.get('notes', '')
            
            # 構建完整的描述
            description = item_name
            if unit:
                description += f" - {unit}"
            
            # 基本驗證
            if not item_name or not amount:
                messages.error(request, '請填寫所有必填欄位')
                return redirect('cost_management')
            
            try:
                amount = float(amount)
                if amount <= 0:
                    messages.error(request, '成本必須大於0')
                    return redirect('cost_management')
            except ValueError:
                messages.error(request, '請輸入有效的成本')
                return redirect('cost_management')
            
            # 處理售價（可選）
            if selling_price:
                try:
                    selling_price = float(selling_price)
                    if selling_price <= 0:
                        messages.error(request, '售價必須大於0')
                        return redirect('cost_management')
                except ValueError:
                    messages.error(request, '請輸入有效的售價')
                    return redirect('cost_management')
            else:
                selling_price = None
            
            from datetime import datetime
            # 創建成本記錄，處理可能的欄位不存在問題
            cost_data = {
                'date': datetime.now(),
                'amount': amount,
                'description': description,
                'category': category,
                'notes': notes,
                'recorded_by': request.user
            }
            
            # 只有在欄位存在時才添加selling_price
            if selling_price is not None:
                cost_data['selling_price'] = selling_price
            
            cost = Cost.objects.create(**cost_data)
            
            messages.success(request, f'成本項目「{item_name}」新增成功！')
            return redirect('cost_management')
            
        except Exception as e:
            messages.error(request, f'新增成本失敗：{str(e)}')
            return redirect('cost_management')
    
    return redirect('cost_management')

@login_required
def add_revenue(request):
    """新增營業額記錄"""
    if request.method == 'POST':
        from sales.models import Sale
        from datetime import datetime
        from django.contrib import messages
        
        try:
            # 獲取表單數據
            amount = request.POST.get('amount')
            category = request.POST.get('category', '')
            notes = request.POST.get('notes', '')
            
            # 驗證必填欄位
            if not amount or float(amount) <= 0:
                messages.error(request, '請輸入有效的成本')
                return redirect('sales_management')
            
            # 創建營業額記錄
            sale = Sale.objects.create(
                date=datetime.now(),
                amount=amount,
                description="營業收入",
                category=category,
                notes=notes,
                recorded_by=request.user
            )
            
            messages.success(request, f'營業額 ${amount} 登記成功！')
            return redirect('sales_management')
            
        except Exception as e:
            messages.error(request, f'營業額登記失敗：{str(e)}')
            return redirect('sales_management')
    
    return redirect('sales_management')

@login_required
def add_expense(request):
    """新增支出記錄"""
    if request.method == 'POST':
        try:
            from expenses.models import Expense
            from datetime import datetime
            
            # 獲取表單數據
            expense_item = request.POST.get('expense_item')
            expense_amount = request.POST.get('expense_amount')
            expense_category = request.POST.get('expense_category', '日常支出')
            expense_notes = request.POST.get('expense_notes', '')
            
            # 驗證必填欄位
            if not expense_item:
                messages.error(request, '請輸入項目名稱')
                return redirect('sales_management')
            
            if not expense_amount or float(expense_amount) <= 0:
                messages.error(request, '請輸入有效的成本')
                return redirect('sales_management')
            
            # 創建支出記錄
            expense = Expense.objects.create(
                date=datetime.now(),
                amount=expense_amount,
                item_name=expense_item,
                category=expense_category,
                notes=expense_notes,
                recorded_by=request.user
            )
            
            messages.success(request, f'支出項目「{expense_item}」記錄成功！')
            return redirect('sales_management')
            
        except Exception as e:
            messages.error(request, f'支出記錄失敗：{str(e)}')
            return redirect('sales_management')
    
    return redirect('sales_management')

@login_required
def edit_sale(request, sale_id):
    """編輯銷售記錄"""
    from sales.models import Sale
    from django.contrib import messages
    from datetime import datetime
    
    try:
        sale = Sale.objects.get(id=sale_id, recorded_by=request.user)
        
        if request.method == 'POST':
            # 更新銷售記錄
            sale.amount = request.POST.get('amount')
            sale.category = request.POST.get('category', '')
            sale.notes = request.POST.get('notes', '')
            
            # 處理日期和時間
            date_str = request.POST.get('date')
            time_str = request.POST.get('time')
            if date_str and time_str:
                datetime_str = f"{date_str} {time_str}"
                sale.date = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
            
            sale.save()
            messages.success(request, '營業額記錄已成功更新！')
            return redirect('sales_management')
        
    except Sale.DoesNotExist:
        messages.error(request, '找不到要編輯的營業額記錄，或您沒有權限編輯此記錄。')
        return redirect('sales_management')
    except Exception as e:
        messages.error(request, f'更新失敗：{str(e)}')
        return redirect('sales_management')

@login_required
def edit_expense(request, expense_id):
    """編輯支出記錄"""
    from expenses.models import Expense
    from django.contrib import messages
    from datetime import datetime
    
    try:
        expense = Expense.objects.get(id=expense_id, recorded_by=request.user)
        
        if request.method == 'POST':
            # 更新支出記錄
            expense.item_name = request.POST.get('expense_item')
            expense.amount = request.POST.get('expense_amount')
            expense.category = request.POST.get('expense_category', '')
            expense.notes = request.POST.get('expense_notes', '')
            
            # 處理日期和時間
            date_str = request.POST.get('date')
            time_str = request.POST.get('time')
            if date_str and time_str:
                datetime_str = f"{date_str} {time_str}"
                expense.date = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
            
            expense.save()
            messages.success(request, '支出記錄已成功更新！')
            return redirect('sales_management')
        
    except Expense.DoesNotExist:
        messages.error(request, '找不到要編輯的支出記錄，或您沒有權限編輯此記錄。')
        return redirect('sales_management')
    except Exception as e:
        messages.error(request, f'更新失敗：{str(e)}')
        return redirect('sales_management')
