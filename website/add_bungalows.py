with app.app_context():
    bungalows = [
        {'id': 1, 'naam': 'Bungalow 1', 'type': '8 personen', 'aantal_personen': 8, 'weekprijs': 1000, 'park_id' : 1},
        {'id': 2, 'naam': 'Bungalow 2', 'type': '8 personen', 'aantal_personen': 8, 'weekprijs': 1000, 'park_id' : 1},
        {'id': 3, 'naam': 'Bungalow 3', 'type': '6 personen', 'aantal_personen': 6, 'weekprijs': 800, 'park_id' : 1},
        {'id': 4, 'naam': 'Bungalow 4', 'type': '6 personen', 'aantal_personen': 6, 'weekprijs': 800, 'park_id' : 1},
        {'id': 5, 'naam': 'Bungalow 5', 'type': '4 personen', 'aantal_personen': 4, 'weekprijs': 600, 'park_id' : 1},
        {'id': 6, 'naam': 'Bungalow 6', 'type': '4 personen', 'aantal_personen': 4, 'weekprijs': 600, 'park_id' : 1},
    ]


    for bungalow_data in bungalows:
            bungalow = Bungalow(
                id=bungalow_data['id'],
                naam=bungalow_data['naam'],
                type=bungalow_data['type'],
                aantal_personen=bungalow_data['aantal_personen'],
                weekprijs=bungalow_data['weekprijs'],
                park_id = bungalow_data['park_id']
            )
            db.session.add(bungalow)
            
            
         db.session.commit()   
