// Обработчик нажатий на клетку
async function clickHandler(id) {
    // Чаще всего getLastReceivedData() это доступные для атаки клетки 
    let attackPositions = getLastReceivedData()
    if (attackPositions != null &&
        attackPositions != 'white' &&
        attackPositions != 'black') {
        // Если это рил доступные клетки для атаки, сверяю, могу ли я сходить куда хочу
        if (attackPositions.some(
            arr => arr[0] == Number(id[0]) && arr[1] == Number(id[2]))
        ) {
            // Если могу, отправляю на сервер запрос о ходе и выполняю move()
            await sendMessage('move|' + getSelectedPosition() + '|' + id)
            await move();
        } else {
            // В противном случае просто выбираю клетку
            selectPosition(id)
        }
    } else {
        selectPosition(id)
    }

}


// Выбор клетки, из которой буду ходить
async function selectPosition(id) {
    await sendMessage('get_color|' + id)
    await checkColor(getLastReceivedData(), id)
}

// Проверяю, можно ли сейчас сходить определенным цветом
async function checkColor(color, id) {
    // Делаем вид, что никакой актуальной информации нет
    setLastReceivedData(null)
    if (color == getNowMove()) {
        setSelectedPosition(id)
        await sendMessage('get_attack_positions|' + id)
        highlighAttackPositions()
    }
}

// Подсвечиваю доступные для атаки клетки
 function highlighAttackPositions() {
    console.log(getLastReceivedData())
    if (getLastReceivedData() != null) {
        // Убираю подсветку старых клеток
        removeHighlighPositions()
        setAttackPositions(getLastReceivedData())
        getLastReceivedData().forEach(array => {
            i = array[0]
            j = array[1]
            cage = document.getElementById(String(i) + '_' + String(j))
            // Добавляем стиль, который подсветит клетку
            cage.classList.add('attack_position')
        });
    }
}

// Убрать подсветку всех клеток
function removeHighlighPositions() {
    for (let i = 1; i < 9; i++) {
        for (let j = 1; j < 9; j++) {
            let cage = document.getElementById(String(i) + '_' + String(j))
            cage.classList.remove('attack_position')
        }
    }
}

function move() {
    // x1 y1 - откуда идет; x2 y2 - куда идет
    let x1 = getSelectedPosition()[0]
    let y1 = getSelectedPosition()[2]
    let x2 = getLastReceivedData().split('|')[2].split('_')[0]
    let y2 = getLastReceivedData().split('|')[2].split('_')[1]

    // Убираю фигуру со стартовой клетки
    let oldCage = document.getElementById(x1 + '_' + y1)
    let images = oldCage.getElementsByTagName('img');

    if (images.length != 0) {
        oldCage.removeChild(images[0]);
    }

    // Убираю фигуру из целевой клетки. если она там есть
    let newCage = document.getElementById(x2 + '_' + y2)
    images = newCage.getElementsByTagName('img');

    if (images.length != 0) {
        newCage.removeChild(images[0]);
    }

    // Устанавливаем нашу фигуру на новую позицию
    let img = document.createElement('img')
    let color = getLastReceivedData().split('|')[0].toLowerCase()
    let name = getLastReceivedData().split('|')[1].toLowerCase()

    img.src = 'site/res/' + color + '_' + name + '.png'
    img.classList.add('figure-image');
    newCage.appendChild(img)

    // После хода убираем позицию
    removeHighlighPositions()

    // Если мат, то перекидывает на финальную страницу
    if (getLastReceivedData().includes('checkmate')) {
        window.location.href = "/win?winner=" + getNowMove()
    }

    // Делаем вид, что никакой актуальной информации нет
    setLastReceivedData(null)
    // Передаем ход
    changeNowMove()
}