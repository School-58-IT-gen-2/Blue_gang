const FIGURES_TO_NUMBERS = {
    '0': 'pawn',
    '1': 'rook',
    '2': 'bishop',
    '3': 'knight',
    '4': 'queen',
    '5': 'king'
}

const COLORS = {
    'w': 'white',
    'b': 'black'
}


function generateChessboard() {
    const chessboard = document.getElementById('chessboard');
    const colors = ['white', 'black']

    for (let row = 0; row < 8; row++){
        const rowElement = document.createElement('tr');
        for (let col = 0; col < 8; col++){
            const cellElement = document.createElement('td');
            cellElement.className = colors[(row + col) % 2];
            cellElement.id = String(row + 1) + '_' + String(col + 1)

            cellElement.addEventListener("click", function () {
                clickHandler(String(row + 1) + '_' + String(col + 1));
            })

            rowElement.appendChild(cellElement);
        }
        chessboard.appendChild(rowElement);
    }
}

function setFigures(figures){
    try{
        figures.forEach(figure => {
            let cage = document.getElementById(
                String(figure[2]) + '_' + String(figure[3]) 
            )
            let imgElement = document.createElement('img');
            imgElement.src = 'site/res/' + figure[1] + '_' + figure[0].toLowerCase() +'.png';
            imgElement.classList.add('figure-image');
            cage.appendChild(imgElement);
    
        });
    } catch (error){
        window.location.href = 'error'
    }
    

}

function decrypt(s){
    let decrypted = [];
    for (let i = 0; i < s.length; i += 4){
        decrypted.push([
            FIGURES_TO_NUMBERS[s[i]], COLORS[s[i + 1]], Number(s[i + 2]), Number(s[i + 3])
        ])
    }
    return decrypted
}


