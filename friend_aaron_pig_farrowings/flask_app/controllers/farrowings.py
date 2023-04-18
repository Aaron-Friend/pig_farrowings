from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.farrowing import Farrowing
from flask_app.models.user import User

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_by_id({'id': session['user_id']})
    if not user:
        return redirect('/logout')
    
    return render_template('dashboard.html', user = user, farrowings = Farrowing.get_all())

@app.route('/view/farrowings_by_sow_id/<int:sow_id>')
def view_sow_id_farrowings(sow_id):
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_by_id({'id': session['user_id']})
    if not user:
        return redirect('/logout')

    return render_template('farrowings_by_sow_id.html', user = user, farrowings = Farrowing.get_by_sow_id({'sow_id': sow_id}))

@app.route('/farrowings/create')
def create_farrowing():
    if 'user_id' not in session:
        return redirect('/logout')
    
    return render_template('new_farrowing.html')

@app.route('/farrowings/create/process', methods = ['POST'])
def process_farrowing():
    print('running sql injection')
    if 'user_id' not in session:
        return redirect('/logout')
    if not Farrowing.validate_farrowing(request.form):
        return redirect('/farrowings/create')
    
    data = {
        'user_id': session['user_id'],
        'sow_id': request.form['sow_id'],
        'date_farrowed': request.form['date_farrowed'],
        'live_born': request.form['live_born'],
        'still_born': request.form['still_born'],
        'mummies': request.form['mummies']
    }
    print(f'inserting data: {data}')
    Farrowing.save(data)
    return redirect('/dashboard')

@app.route('/view/farrowings/<int:id>')
def view_farrowing(id):
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('view_farrowing.html', farrowing = Farrowing.get_by_id({'id': id}))

@app.route('/edit/farrowings/<int:id>')
def edit_farrowing(id):
    if 'user_id' not in session:
        return redirect('/')
    return render_template('edit_farrowing.html', farrowing = Farrowing.get_by_id({'id': id}))



@app.route('/edit/farrowings/process/<int:id>', methods = ['POST'])
def process_edit(id):
    if 'user_id' not in session:
        return redirect('/')
    if not Farrowing.validate_farrowing(request.form):
        return redirect('/edit/farrowings/{id}')
    
    data = {
        'id': id,
        'sow_id': request.form['sow_id'],
        'date_farrowed': request.form['date_farrowed'],
        'live_born': request.form['live_born'],
        'still_born': request.form['still_born'],
        'mummies': request.form['mummies']
    }
    Farrowing.edit(data)
    return redirect('/dashboard')

@app.route('/farrowings/delete/<int:id>')
def delete_farrowing(id):
    if 'user_id' not in session:
        return redirect('/')
    Farrowing.delete({'id': id})
    return redirect('/dashboard')