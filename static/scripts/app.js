console.log('test4')
console.log('test')

console.log('test2')
// profile menu
console.log(document.getElementById('profile-icon'))
document.getElementById('profile-icon').
    addEventListener('click', () => {
        console.log('from func')
        document.getElementById('profile-choices').style.display = 'block'
    })
