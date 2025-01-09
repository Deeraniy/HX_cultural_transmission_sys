// 模拟数据
const books = [
    { image: '../src/assets/folkCustom/汨罗江端午习俗.jpg', content: 'Content for page 2', category: '非遗' },
    { image: '../src/assets/folkCustom/湘昆.jpg', content: 'Content for page 2', category: '非遗' },
    { image: '../src/assets/folkCustom/湘剧.jpg', content: 'Content for page 2', category: '非遗' },
    { image: '../src/assets/folkCustom/皮影戏.jpg', content: 'Content for page 2', category: '非遗' },
    { image: '../src/assets/folkCustom/湘绣.jpg', content: 'Content for page 2', category: '非遗' },
    { image: '../src/assets/folkCustom/赶尸.png', content: 'Content for page 2', category: '民俗' },
    { image: '../src/assets/folkCustom/湖南傩戏.jpg', content: 'Content for page 2', category: '民俗' }
];

// 当前页和每页展示的书籍数
let currentPage = 0;
const booksPerPage = 3;

// 处理搜索和过滤
const searchTermInput = document.getElementById('searchTerm');
const selectedCategorySelect = document.getElementById('selectedCategory');
const applyFiltersButton = document.getElementById('applyFilters');
const bookshelfContainer = document.getElementById('bookshelfContainer');
const prevPageButton = document.getElementById('prevPage');
const nextPageButton = document.getElementById('nextPage');

// 过滤书籍函数
function filterBooks() {
    const searchTerm = searchTermInput.value.toLowerCase();
    const selectedCategory = selectedCategorySelect.value;

    return books.filter(book => {
        const matchesSearchTerm = book.content.toLowerCase().includes(searchTerm) || book.category.toLowerCase().includes(searchTerm);
        const matchesCategory = selectedCategory ? book.category === selectedCategory : true;
        return matchesSearchTerm && matchesCategory;
    });
}

// 更新书架显示
function updateBookshelf() {
    const filteredBooks = filterBooks();
    const totalPages = Math.ceil(filteredBooks.length / booksPerPage);
    const start = currentPage * booksPerPage;
    const end = start + booksPerPage;
    const booksToDisplay = filteredBooks.slice(start, end);

    bookshelfContainer.innerHTML = ''; // 清空现有书架内容

    // 渲染书架
    booksToDisplay.forEach(book => {
        const bookElement = document.createElement('div');
        bookElement.classList.add('sample');
        bookElement.style.backgroundImage = `url(${book.image})`;
        bookElement.addEventListener('click', () => onBookClick(book));
        bookshelfContainer.appendChild(bookElement);
    });

    // 更新分页按钮状态
    prevPageButton.disabled = currentPage === 0;
    nextPageButton.disabled = currentPage >= totalPages - 1;
}

// 处理翻页
function prevPage() {
    if (currentPage > 0) {
        currentPage--;
        updateBookshelf();
    }
}

function nextPage() {
    currentPage++;
    updateBookshelf();
}

// 处理点击书籍事件
function onBookClick(book) {
    const hoveredBook = book; // 设置当前查看的书籍
    document.getElementById('editor').textContent = hoveredBook.editor || '';
    document.getElementById('isbn').textContent = hoveredBook.isbn || '';
    document.getElementById('publisher').textContent = hoveredBook.publisher || '';
    document.getElementById('price').textContent = hoveredBook.price || '';
    document.getElementById('category').textContent = hoveredBook.category || '';
    document.getElementById('content').textContent = hoveredBook.content || '';
    document.getElementById('format').textContent = hoveredBook.format || '';
    document.getElementById('folkObject').src = hoveredBook.image || 'https://img.dpm.org.cn/Uploads/image/2024/12/18/出版推荐448-546汉英日历-XHuSkowdJ260.png';
}

// 初始化
applyFiltersButton.addEventListener('click', updateBookshelf);
prevPageButton.addEventListener('click', prevPage);
nextPageButton.addEventListener('click', nextPage);

// 初始加载
updateBookshelf();
