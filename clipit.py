from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont

# Couleurs
bleu = "#1423DC"
blanc = "#ffffff"
# Fonts
bold = ImageFont.truetype("sources/fonts/Enedis-Bold.ttf", 74)
# Dimensions
pb = 18
h_ligne = 86
h_grille = 180
ph = 36
ml = 90
mb = 22

# Fonctions
def ecrire_ligne_titre(draw, index, texte):
    box = draw.textbbox((ml + ph, 2 * h_grille + index * (h_ligne + mb)), texte, anchor="ls", font=bold)
    draw.rectangle([(ml, 2 * h_grille + pb - 1 + index * (h_ligne + mb)), (box[2] + ph, 2 * h_grille + pb - h_ligne + index * (h_ligne + mb))], blanc)
    draw.text((ml + ph, 2 * h_grille + index * (h_ligne + mb)), texte, fill=bleu, anchor="ls", font=bold)

def creer_image_titre(nom, texte):
    im = Image.new("RGBA", (1080, 1080))
    draw = ImageDraw.Draw(im)
    draw.rectangle([(0, 0), (1080, 1080)], bleu)
    for i, ligne in enumerate(texte):
        ecrire_ligne_titre(draw, i, ligne)
    im.save(f"intermediaires/{nom}.png")
    im.close()

def importer_clip(nom):
    clip = VideoFileClip(nom, has_mask=True)
    original_size = clip.size
    if original_size != [1080, 1080]:
        print(f"resizing clip {nom}")
        clip = VideoClip.crop(clip, width=1080, height=1080, x_center=original_size[0]/2, y_center=original_size[1]/2)
    return clip

# Début exécution
print("starting")
liste_clips = []
duree_actuelle = 0

# Intro
intro = importer_clip("sources/videos/1x1/intro 3s.mov").set_layer(2)
liste_clips.append(intro)
duree_actuelle += 2

# Titre
creer_image_titre('titre', ["Le compteur linky,", "un outil pour", "la transition écologique"])
titre = ImageClip("intermediaires/titre.png", duration=5).set_start(duree_actuelle)
liste_clips.append(titre)
fil = ImageClip("sources/img/Fil_blanc.jpg", duration=titre.duration).set_start(duree_actuelle).set_layer(1)
fil = fil.set_position(lambda t: (pow(100, t-4) * 300, 2*h_grille+2*h_ligne+2*mb+pb+60))
liste_clips.append(fil)
carre = ImageClip("sources/img/blue.jpg", duration=titre.duration).set_start(duree_actuelle).set_layer(1)
carre = carre.set_position(lambda t: (pow(100, t-4.2) * 300 - 1080 if (pow(100, t-4.2) * 300) < 1080 else 0, 0))
liste_clips.append(carre)
duree_actuelle += titre.duration

# Corps du clip
clip = importer_clip('test.mp4').set_layer(0).subclip(0,4).set_start(duree_actuelle)
liste_clips.append(clip)
duree_actuelle += clip.duration

# Outro
outro = importer_clip("sources/videos/1x1/outro 3s.mov").set_layer(1).set_start(duree_actuelle-0.5)
liste_clips.append(outro)

# Montage final
video = CompositeVideoClip(liste_clips)
video.write_videofile('output.mp4')

# Fermeture des clips
for clip in liste_clips:
    clip.close()