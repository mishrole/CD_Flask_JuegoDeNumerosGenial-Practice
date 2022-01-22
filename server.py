from flask import Flask, render_template, request, redirect, session
import random

app = Flask( __name__ )
app.secret_key = 'coding dojo is awesome'

# Limpia todo excepto la lista de ganadores
def resetGame():
    if 'winners' in session:
        winners = session['winners']
    else:
        winners = []

    session.clear()
    session['winners'] = winners

# Genera las cookies iniciales y renderiza la plantilla de juego
@app.route( '/', methods=['GET'] )
def game():
    if not 'winners' in session:
        session['winners'] = []

    if not 'max_attemps' in session:
        session['max_attemps'] = 5
    
    if not 'current_attemps' in session:
        session['current_attemps'] = 0

    if not 'hint_text' in session:
        session['hint_text'] = "Are you ready?"
    
    if not 'hint_color' in session:
        session['hint_color'] = "bg-primary"

    if not 'randomNumber' in session:
        session['randomNumber'] = random.randint(1, 100)
        print(session['randomNumber'])
    else:
        print(session['randomNumber'])

    if not 'game_status' in session:
        session['game_status'] = "progress"

    return render_template( "game.html", hint_text = session['hint_text'], hint_color = session['hint_color'], game_status = session['game_status'], max_attemps = session['max_attemps'], current_attemps = session['current_attemps'])

# Determina el resultado del juego y sobreescribe las cookies de estado
@app.route( '/guess', methods=['POST'] )
def guess():
    if 'current_attemps' in session and 'max_attemps' in session:
        if int(session['current_attemps']) <= int(session['max_attemps']):

            if request.form['inputGuess'].isnumeric():
                attempt = int(request.form['inputGuess'])

                if 'randomNumber' in session:
                    randomNumber = int(session['randomNumber'])

                    if randomNumber == attempt:
                        session['hint_text'] = f"You guessed it! {randomNumber} was the number"
                        session['hint_color'] = "bg-success"
                        session['game_status'] = "win"
                    elif attempt < randomNumber:
                        session['hint_text'] = "Too low!"
                        session['hint_color'] = "bg-danger"
                    elif attempt > randomNumber:
                        session['hint_text'] = "Too high!"
                        session['hint_color'] = "bg-danger"
                else:
                    return redirect('/reset')

                session['current_attemps'] = int(session['current_attemps']) + 1

            else:
                session['hint_text'] = f"😓 '{request.form['inputGuess']}' is not a number between 1 and 100 😓"
                session['hint_color'] = "bg-warning"

            if int(session['current_attemps']) == int(session['max_attemps']) and session['game_status'] != "win":
                session['hint_text'] = "🤡 Oh... I guess you lost 🤡"
                session['hint_color'] = "bg-secondary"
                session['game_status'] = "end"

    return redirect('/')

# Limpia todo excepto la lista de ganadores
@app.route( '/reset', methods=['GET'])
def reset():
    resetGame()
    return redirect('/')

# Guarda el ganador actual, ordena la lista de menor a mayor en base al puntaje, y redirecciona a la lista de ganadores
@app.route( '/save', methods=['POST'])
def save():
    player = request.form['inputPlayer']
    attemps = int(session['current_attemps'])

    winner = {
        "name": player,
        "score": attemps
    }

    winners = session['winners']
    winners.append(winner)
    newlist = sorted(winners, key=lambda d: d['score']) 
    session['winners'] = newlist

    resetGame()

    return redirect('/winners')

# Renderiza la lista de ganadores
@app.route( '/winners', methods=['GET'])
def winners():
    if not 'winners' in session:
        session['winners'] = []

    return render_template( "winners.html", winners = session['winners'])

if __name__ == "__main__":
    app.run( debug = True )