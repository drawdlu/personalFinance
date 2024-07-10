window.onload = function() {
    let buttonEdit = document.querySelectorAll('.confirm-edit');
    buttonEdit.forEach(a => a.addEventListener("click", b=>{
        return confirm('Are you sure you want to edit this?');
    }))

    let buttonDelete = document.querySelectorAll('.confirm-delete');
    buttonDelete.forEach(a => a.addEventListener("click", b=>{
        return confirm('Are you sure you want to delete this?');
    }))
}

