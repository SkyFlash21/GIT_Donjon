def verif_room_connector(matrice):
    verification_global = True
    direction = [(1,0),(-1,0),(0,1),(0,-1)]
    shape = matrice.shape
    for posy in range(shape[0]):
        for posx in range(shape[1]):
            for posz in range(shape[2]):
                if matrice[posy,posx,posz] == 5:
                    valide = False
                    for face in direction:
                        if matrice[posy,posx+face[0],posz+face[1]] == 0:
                            valide = True
                            break
                    if not valide:
                        verification_global = False
    return verification_global
