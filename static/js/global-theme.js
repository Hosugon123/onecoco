// 一口口麻辣串記帳系統 - 全局主題JavaScript

// 主題切換功能
function toggleTheme() {
    const body = document.body;
    const themeIcon = document.getElementById('theme-icon');
    const themeText = document.getElementById('theme-text');
    
    // 檢查當前是否為深色主題
    const isCurrentlyDark = body.hasAttribute('data-theme') && body.getAttribute('data-theme') === 'dark';
    
    console.log('當前是否為深色主題:', isCurrentlyDark);
    
    if (isCurrentlyDark) {
        // 切換到淺色主題
        body.removeAttribute('data-theme');
        if (themeIcon) themeIcon.textContent = '🌙';
        if (themeText) themeText.textContent = '深色';
        localStorage.setItem('theme', 'light');
        console.log('切換到淺色主題');
    } else {
        // 切換到深色主題
        body.setAttribute('data-theme', 'dark');
        if (themeIcon) themeIcon.textContent = '☀️';
        if (themeText) themeText.textContent = '淺色';
        localStorage.setItem('theme', 'dark');
        console.log('切換到深色主題');
    }
    
    // 強制重新計算樣式
    const computedStyle = window.getComputedStyle(body);
    console.log('當前背景色:', computedStyle.backgroundColor);
    console.log('當前文字色:', computedStyle.color);
    console.log('data-theme 屬性:', body.getAttribute('data-theme'));
}

// 載入保存的主題
function loadTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    console.log('載入主題:', savedTheme);
    
    const body = document.body;
    const themeIcon = document.getElementById('theme-icon');
    const themeText = document.getElementById('theme-text');
    
    if (savedTheme === 'dark') {
        body.setAttribute('data-theme', 'dark');
        if (themeIcon) themeIcon.textContent = '☀️';
        if (themeText) themeText.textContent = '淺色';
        console.log('應用深色主題');
    } else {
        body.removeAttribute('data-theme');
        if (themeIcon) themeIcon.textContent = '🌙';
        if (themeText) themeText.textContent = '深色';
        console.log('應用淺色主題');
    }
}

// 頁面載入時應用保存的主題
document.addEventListener('DOMContentLoaded', function() {
    console.log('頁面載入完成，初始化主題功能');
    
    // 立即應用主題
    loadTheme();
    
    // 為主題切換按鈕添加事件監聽器
    const themeButton = document.getElementById('theme-toggle-btn');
    if (themeButton) {
        console.log('找到主題切換按鈕，添加事件監聽器');
        themeButton.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('主題切換按鈕被點擊');
            toggleTheme();
        });
    }
    
    // 確保全局函數可用
    window.toggleTheme = toggleTheme;
    console.log('主題切換功能已初始化');
});

// 通用工具函數
const Utils = {
    // 格式化金額
    formatCurrency: function(amount) {
        return new Intl.NumberFormat('zh-TW', {
            style: 'currency',
            currency: 'TWD'
        }).format(amount);
    },
    
    // 格式化日期
    formatDate: function(date) {
        return new Intl.DateTimeFormat('zh-TW', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        }).format(new Date(date));
    },
    
    // 顯示消息
    showMessage: function(message, type = 'info') {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        messageDiv.textContent = message;
        
        const messagesContainer = document.querySelector('.messages') || document.body;
        messagesContainer.insertBefore(messageDiv, messagesContainer.firstChild);
        
        // 3秒後自動移除
        setTimeout(() => {
            messageDiv.remove();
        }, 3000);
    },
    
    // 確認對話框
    confirm: function(message, callback) {
        if (confirm(message)) {
            callback();
        }
    },
    
    // 防抖函數
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
};

// 表格相關功能
const TableUtils = {
    // 篩選表格
    filterTable: function(inputId, tableId) {
        const input = document.getElementById(inputId);
        const table = document.getElementById(tableId);
        
        if (!input || !table) return;
        
        const filter = input.value.toLowerCase();
        const rows = table.getElementsByTagName('tr');
        
        for (let i = 1; i < rows.length; i++) {
            const row = rows[i];
            const cells = row.getElementsByTagName('td');
            let found = false;
            
            for (let j = 0; j < cells.length; j++) {
                const cell = cells[j];
                if (cell.textContent.toLowerCase().indexOf(filter) > -1) {
                    found = true;
                    break;
                }
            }
            
            row.style.display = found ? '' : 'none';
        }
    },
    
    // 排序表格
    sortTable: function(tableId, columnIndex) {
        const table = document.getElementById(tableId);
        if (!table) return;
        
        const rows = Array.from(table.getElementsByTagName('tr'));
        const header = rows[0];
        const dataRows = rows.slice(1);
        
        const isAscending = table.getAttribute('data-sort-direction') !== 'asc';
        
        dataRows.sort((a, b) => {
            const aVal = a.cells[columnIndex].textContent.trim();
            const bVal = b.cells[columnIndex].textContent.trim();
            
            // 嘗試數字比較
            const aNum = parseFloat(aVal.replace(/[^\d.-]/g, ''));
            const bNum = parseFloat(bVal.replace(/[^\d.-]/g, ''));
            
            if (!isNaN(aNum) && !isNaN(bNum)) {
                return isAscending ? aNum - bNum : bNum - aNum;
            }
            
            // 字符串比較
            return isAscending ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal);
        });
        
        // 重新排列行
        dataRows.forEach(row => table.appendChild(row));
        table.setAttribute('data-sort-direction', isAscending ? 'asc' : 'desc');
    }
};

// 表單相關功能
const FormUtils = {
    // 驗證表單
    validateForm: function(formId) {
        const form = document.getElementById(formId);
        if (!form) return false;
        
        const requiredFields = form.querySelectorAll('[required]');
        let isValid = true;
        
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                field.classList.add('error');
                isValid = false;
            } else {
                field.classList.remove('error');
            }
        });
        
        return isValid;
    },
    
    // 重置表單
    resetForm: function(formId) {
        const form = document.getElementById(formId);
        if (form) {
            form.reset();
            const errorFields = form.querySelectorAll('.error');
            errorFields.forEach(field => field.classList.remove('error'));
        }
    }
};

// 模態框相關功能
const ModalUtils = {
    // 顯示模態框
    showModal: function(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.style.display = 'block';
            document.body.style.overflow = 'hidden';
        }
    },
    
    // 隱藏模態框
    hideModal: function(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    },
    
    // 初始化模態框
    initModal: function(modalId, triggerId, closeId) {
        const modal = document.getElementById(modalId);
        const trigger = document.getElementById(triggerId);
        const close = document.getElementById(closeId);
        
        if (trigger) {
            trigger.addEventListener('click', () => this.showModal(modalId));
        }
        
        if (close) {
            close.addEventListener('click', () => this.hideModal(modalId));
        }
        
        // 點擊模態框外部關閉
        if (modal) {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    this.hideModal(modalId);
                }
            });
        }
    }
};

// 導出全局對象
window.ThemeUtils = {
    toggleTheme,
    loadTheme
};

window.Utils = Utils;
window.TableUtils = TableUtils;
window.FormUtils = FormUtils;
window.ModalUtils = ModalUtils;
