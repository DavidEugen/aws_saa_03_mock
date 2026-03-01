// Setup page JavaScript

let groupCounter = 0;

document.addEventListener('DOMContentLoaded', function() {
    // Select/Deselect all categories
    const selectAllBtn = document.getElementById('selectAllCategories');
    if (selectAllBtn) {
        selectAllBtn.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelectorAll('.category-checkbox').forEach(checkbox => {
                checkbox.checked = true;
            });
        });
    }

    const deselectAllBtn = document.getElementById('deselectAllCategories');
    if (deselectAllBtn) {
        deselectAllBtn.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelectorAll('.category-checkbox').forEach(checkbox => {
                checkbox.checked = false;
            });
        });
    }

    // Add keyword group
    const addGroupBtn = document.getElementById('addGroupButton');
    if (addGroupBtn) {
        addGroupBtn.addEventListener('click', function(e) {
            e.preventDefault();
            addKeywordGroup();
        });
    }

    // Add initial empty group if desired, or leave empty
    // addKeywordGroup();
});

function addKeywordGroup() {
    const groupsContainer = document.getElementById('keywordGroups');

    const groupDiv = document.createElement('div');
    groupDiv.className = 'keyword-group';
    groupDiv.dataset.groupId = groupCounter;

    const header = document.createElement('div');
    header.className = 'group-header';
    header.innerHTML = `
        <span class="group-title">그룹 ${groupCounter + 1}</span>
        <button type="button" class="btn-delete-group" onclick="deleteGroup(${groupCounter})">그룹 삭제</button>
    `;


    const keywordsContainer = document.createElement('div');
    keywordsContainer.className = 'keywords-container';
    keywordsContainer.id = `group_${groupCounter}_keywords_container`;

    const currentGroupId = groupCounter;

    const addKeywordBtn = document.createElement('button');
    addKeywordBtn.type = 'button';
    addKeywordBtn.className = 'btn-add-keyword';
    addKeywordBtn.textContent = '키워드 추가';
    addKeywordBtn.onclick = function(e) {
        e.preventDefault();
        addKeyword(currentGroupId);
    };

    groupDiv.appendChild(header);
    groupDiv.appendChild(keywordsContainer);
    groupDiv.appendChild(addKeywordBtn);

    groupsContainer.appendChild(groupDiv);
    
    
    // Add one empty keyword input
    addKeyword(groupCounter);

    groupCounter++;
    updateGroupCount();
}

function addKeyword(groupId) {
    const container = document.getElementById(`group_${groupId}_keywords_container`);

    const keywordItem = document.createElement('div');
    keywordItem.className = 'keyword-item';

    const input = document.createElement('input');
    input.type = 'text';
    input.className = 'keyword-input';
    input.name = `group_${groupId}_keywords`;
    input.placeholder = '키워드 입력';

    const deleteBtn = document.createElement('button');
    deleteBtn.type = 'button';
    deleteBtn.className = 'btn-delete-keyword';
    deleteBtn.textContent = '삭제';
    deleteBtn.onclick = function(e) {
        e.preventDefault();
        keywordItem.remove();
    };

    keywordItem.appendChild(input);
    keywordItem.appendChild(deleteBtn);
    container.appendChild(keywordItem);
}

function deleteGroup(groupId) {
    const groupDiv = document.querySelector(`[data-group-id="${groupId}"]`);
    if (groupDiv) {
        groupDiv.remove();
    }
}

function updateGroupCount() {
    document.getElementById('groupCount').value = groupCounter;
}

// Form submission validation
document.addEventListener('DOMContentLoaded', function() {
    const setupForm = document.getElementById('setupForm');
    if (setupForm) {
        setupForm.addEventListener('submit', function(e) {
            const selectedCategories = document.querySelectorAll('.category-checkbox:checked').length;

            if (selectedCategories === 0) {
                e.preventDefault();
                alert('최소 1개 이상의 카테고리를 선택해주세요.');
                return false;
            }
        });
    }
});
