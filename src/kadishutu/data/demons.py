from .csvutils import make_maps_dict


DEMONS = [
    {"id": 1, "name": "Satan",
     "lore": """A Judeo-Christian angel of darkness
with a name that means "adversary."
Also known as the evil serpent that
tempted Adam and Eve in the Garden
of Eden. In the Book of Job, he is
depicted as a servant of God who
tests Job, a man of faith, and is said
to be the accuser angel sent from
the heavens to judge mankind."""},
    {"id": 2, "name": "Lucifer",
     "lore": """The Lord of Chaos who leads
the fallen angels and, according
to Christian tradition, is equated
with Satan.
His name holds the meaning of
"one who brings light" indicating
that he was once the most beautiful
of the archangels. However, it is said
that he rebelled against the almighty
Creator and chose to become a fallen
angel."""},
    {"id": 4, "name": "Dagda",
     "lore": "TODO"},
    {"id": 7, "name": "Khonsu",
     "lore": """The Egyptian god of the moon.
Often portrayed as a mummy with
two long braids of hair, he is said
to be a reincarnation of the moon
itself and holds possession over
what's known as the moon ship.
He also acts as a companion to
the Pharaoh's shadow. Hieroglyphics 
found in Unas's pyramid depict him
as a god who prepares meals for an
oppressive, god-devouring king."""},
    {"id": 8, "name": "Zeus",
     "lore": """The main deity of Greek mythology.
Said to be omnipotent, he is both
god of the sky and ruler of the
twelve gods of Olympus.
He is a son of the titan Kronos and
brother to both Hades and Poseidon.
Upon defeating his father, he claimed
the right to rule the entire universe.
He also fathered many children with
not only goddesses, but a number of
human women as well."""},
    {"id": 9, "name": "Odin",
     "lore": """The All-Father in Norse Mythology.
Warrior, sorcerer, and near insatiable
seeker of knowledge, he rides
his eight-legged horse Sleipnir, armed
with both Gungnir, his mighty spear,
and Draupnir, an enchanted ring.
He is known to have willingly
sacrificed an eye to drink from
the Well of Wisdom and is also
recognized as the one who welcomes
the souls of departed warriors
as they cross over into Valhalla."""},
    {"id": 11, "name": "Mitra",
     "lore": """Commonly known as Mitra-Buddha
or Mitra.
An ancient Persian god of contracts,
he was also revered as a sun god. He
is a protector of the world's harmony
and truth and passes judgment upon
those who threaten it. It is said that
one of his powers to safeguard
harmony allows him to cure any
illness."""},
    {"id": 12, "name": "Atavaka",
     "lore": """One of the eight Yasha-o.
His domain is war and protection.
Originally known as a wicked
devourer of children, he later became
one of the greatest of the Wisdom
Kings after receiving the Buddha's
enlightenment."""},
    {"id": 13, "name": "Horus",
     "lore": """An ancient god of Egypt known for
having the sun and moon as his
watchful eyes.
He was revered by some as the
principle god, most likely due to
his association with the celestial
bodies above. Myth often depicts
him as a hawk or a falcon."""},
    {"id": 14, "name": "Thoth",
     "lore": """An almighty god of Egyptian lore with
the head of a baboon. He stands
opposite Seth, the god of evil, and
sides with Osiris and Isis, the gods of
good."""},
    {"id": 15, "name": "Khonsu Ra",
     "lore": """The form of the Egyptian god of
the Moon, Khonsu, upon gaining
the power of the sun god, Ra.
Hidden behind a foreboding mask,
he possesses the dual powers of the
sun and moon, the day and night, and
the living and the dead."""},
    {"id": 16, "name": "Vishnu",
     "lore": """One of the Trimurti and the
highest-ranking god in Hinduism.
He governs the universe and is also
recognized as its protector. It is said
that when the surface world is in
danger, he will appear as an avatar."""},
    {"id": 17, "name": "Baal",
     "lore": """The chief Semitic god.
Bearing a name that means "Lord,"
or "owner," he was revered as a god
of fertility in addition to being known
as the god of Canaan and both
brother and consort to the goddess
Anat. Many demons, such as Bael,
Beelzebub, Belphegor, and Berith, are
believed to be derivations of Baal.
There were even instances of him
being worshiped in the very same
temples as Yahweh (YHVH) in times
long since passed."""},
    {"id": 19, "name": "Demeter",
     "lore": """A goddess from Greek mythology.
Her name means "Mother Earth"
in ancient Greek.
She is the sister of Zeus, the goddess
of fertility, and is said to be the one
who taught humanity the ways of
agriculture. With the advancement
of civilization, laws were put into
place, and she was given another
name: \"Demeter Thesmophoros.\""""},
    {"id": 20, "name": "Anahita",
     "lore": """A Zoroastrian goddess whose name
means "pure."
While primarily known as a beautiful
deity who rules over rivers and
water, she is also the goddess of
health, fertility, safe delivery,
production of livestock, harvest,
wealth, and expansion of land. She is
often portrayed as an elegant virgin
wearing a crown decorated with
numerous stars in addition to a
golden necklace and a golden cape,
and is typically shown holding a
water jug. She is also a brave god of
war astride a four-wheeled chariot,
toppling demons and tyrants alike.
Both her allies and her enemies have
been said to have offered their
prayers to her."""},
    {"id": 21, "name": "Lakshmi",
     "lore": """The goddess of beauty and good
fortune in Hindu lore.
Vishnu's wife and Kama's mother,
she is regarded as the goddess
of love and is said to embody
the ideal woman. She is also
known to have charmed many
gods with her dance."""},
    {"id": 22, "name": "Norn",
     "lore": """The goddesses of fate in Norse myth.
They live below the roots of Yggdrasil
and weave the threads of fate by
which even the gods are bound."""},
    {"id": 23, "name": "Idun",
     "lore": """A goddess from Norse mythology.
She is the keeper of the golden
apples and wife to Bragi, the god of
poetry.
Gods in Norse mythology are said
to retain their youth via her apples,
which are safely kept in a box made
from ash wood."""},
    {"id": 24, "name": "Sarasvati",
     "lore": """The consort of Brahma in Hindu lore.
She embodies the river, and her name
means "one who flows." She is also
the goddess of music and art and is
said to be skilled in every artistic or
creative pursuit known to man."""},
    {"id": 25, "name": "Ishtar",
     "lore": """A Mesopotamian goddess of love
and war. She was dubbed the Queen
of Heaven, and the planet Venus was
often seen as the embodiment of
the goddess herself.
In the "Epic of Gilgamesh," she makes
many heroes her lovers, but the story
also foretells of their unfortunate fate
by her hands: eventual death or
transformation into animals."""},
    {"id": 26, "name": "Scathach",
     "lore": """The war goddess of Celtic lore as well
as the queen of the Land of Shadows.
She is a skilled magician and a master
warrior who trains the many young
men who come to her in the art of
war. The famed Cu Chulainn was one
of her students, and it is said that he
received the legendary Gae Bolg
from her upon mastering her
teachings."""},
    {"id": 27, "name": "Parvati",
     "lore": """This beautiful goddess of love is one
of Shiva's wives in Hindu mythology.
She won Shiva's love despite the fact
that he was an ascetic."""},
    {"id": 28, "name": "Ame-no-Uzume",
     "lore": """The goddess of entertainment in
Japanese lore.
She governs many sacred dances
and is most famous for
the provocative dance she used to
lure out Amaterasu, who had
barricaded herself inside a cave. She
later became Sarutahiko's wife."""},
    {"id": 29, "name": "Fortuna",
     "lore": """The Roman goddess of luck, she
spins the Wheel of Fortune and is
believed to have originally been a
fertility goddess. Her Greek
counterpart is Tyche."""},
    {"id": 30, "name": "Maria",
     "lore": """The maternal figure of Christianity.
Gabriel informed her that she was to
be the mother of Jesus. Some sects
revere her as the Virgin Mary, but
other denominations do not focus
on her."""},
    {"id": 31, "name": "Artemis",
     "lore": """The Greek goddess of hunting and
chastity. She was often identified
with the moon goddess Selene and
was therefore also worshiped as a
moon goddess herself.
Like her twin brother Apollo,
her association with archery granted
her the title of "far-shooter" in
addition to being recognized as
a bringer of plague and death.
This is depicted in myth, in which
she is deceived by Apollo and shoots
her beloved Orion."""},
    {"id": 32, "name": "Konohana Sakuya",
     "lore": """One of the Kunitsukami in Japanese
mythology. Daughter of
Oyamatsumi.
Younger sister of Iwanaga-hime.
Her name means "a woman who
blooms and flourishes like a cherry
blossom." She is considered one of
the most beautiful of Japan's myriad
gods. She fell in love with Ninigi of
the Amatsukami and became his
wife. After she became pregnant in
just one night, he questioned
whether the child was truly his, and
therefore godly. As proof that the
child was of the Amatsukami, she
barricaded herself in a birthing-house
and set it on fire, then successfully
gave birth. Originally, she is said to
have been a god who governed
water. However, this legacy of giving
birth in a fire earned her regard as
the goddess of volcanoes, and she is
identified with the volcano spirit
Asama no Okami."""},
    {"id": 34, "name": "Hanuman",
     "lore": """A hero of Hindu descent. He can
transform into anything, fly, and
possesses incredible strength.
He performed many heroic deeds in
the epic "Ramayana" and is almost
always depicted as a monkey."""},
    {"id": 35, "name": "Fionn Mac Cumhaill",
     "lore": """The leader of the Fianna, warriors
who protected High King Cormac of
Ireland. He was born as Deimne, but
due to his blond hair and white skin,
he soon came to be called "Fionn,"
a name meaning "golden hair."
When training under the druid
Finn Eces, he was ordered to cook
the Salmon of Knowledge. Upon
licking some of the salmon's fat from
his thumb, he gained its knowledge.
From that point on, it is said that
Fionn could tap this knowledge any
time he licked his thumb."""},
    {"id": 36, "name": "Cu Chulainn",
     "lore": """A gallant Celtic hero and son of the
sun god Lugh.
He is said to have beaten a whole
army singlehandedly. He was cursed
to die after spurning the war goddess
Morrigan and was impaled on his
own mighty spear, Gae Bolg."""},
    {"id": 37, "name": "Kurama Tengu",
     "lore": """A tengu that is said to have lived in
Mt. Kurama in Kyoto.
The most powerful and well-known
of the tengu, he has the power to
fend off disease and bring good
fortune. He is also said to have
trained Yoshitsune how to fight with
a sword when Yoshitsune was still
a child. Some believe him to be
Bishamonten's night form."""},
    {"id": 38, "name": "Amanozako",
     "lore": """A Japanese goddess commonly
thought to be the ancestor of the
tengu and amanojaku.
The famed warrior Susano-o once
allowed his tempestuous spirit to
build up to such an intense degree,
he vomited her out as a result.
Similarly to Susano-o, she has a wild
personality and tends to go on a
rampage if she doesn't get her way.
It is said that she can hurl even the
most powerful gods a great distance,
and that her fangs can mangle the
very sharpest of blades. Like
amanojaku, she is prone to doing the
exact opposite of what is expected."""},
    {"id": 40, "name": "Kresnik",
     "lore": """A virtuous vampire hunter blessed
by the power of light. His name
comes from the word "cross."
Archnemesis of a Slovenian vampire,
Kudlak, with whom he engages in
endless conflict. Both of them fight
by transforming into animals such as
pigs, bulls, and horses, but Kresnik's
bestial forms are always pure white
in color. Kudlak, the enemy of
God, is never considered to be
a match for the emissary of light,
and their battles always end with
Kresnik's victory."""},
    {"id": 41, "name": "Anansi",
     "lore": """A folkloric hero of the Ashanti and
other tribes in West Africa. He is
depicted as a trickster who gets by
on his wit and cunning. Portrayed as
a spider or a man, depending on
interpretation.
Anansi appears in many stories,
including one where he collects
the people's wisdom in a gourd and
attempts to hang it from a tree. But
in a fit of dismay, he upends it
and scatters wisdom across the
world. Other stories tell of how he
buys the stories of the sky god
Onyankopon and makes them his
own. These stories are collectively
called Anansesem, or spider tales."""},
    {"id": 42, "name": "Koppa Tengu",
     "lore": """A smaller member of the Tengu race
less powerful than other Tengu.
They are believed to be an
incarnation of an old wolf and are
capable of eventually transforming
into Karasu Tengu."""},
    {"id": 43, "name": "Apsaras",
     "lore": """Water spirits in Hindu lore.
They are beautiful young women who
dance for the gods. They also guide
heroes who fall in battle to paradise."""},
    {"id": 44, "name": "Agathion",
     "lore": """A familiar with no physical body that
appears only during the day.
There is no consensus on the
appearance of an Agathion: it can
resemble a human, bird, or animal.
They are usually sealed away in
bottles or pots but can also be sealed
in rings or talismans. The term
Agathion is also used as a general
term for familiars."""},
    {"id": 45, "name": "Mandrake",
     "lore": """A magical plant whose roots take the
appearance of a human.
Mandrakes are a precious component
in potions to heal sicknesses, but
obtaining one is notoriously difficult.
When pulled from the ground, they
let out a bloodcurdling scream, killing
anyone unlucky enough to hear it.
There are both male and female
variations of Mandrakes."""},
    {"id": 46, "name": "Dis",
     "lore": """Figures in Norse mythology
considered to be spiritual
companions of humans.
While they are said to be protectors
of agriculture and livestock, they are
also noted as masters of war. They
are sometimes regarded as spirits
that accompany the Valkyrie, or play
a similar role. Also interpreted as
lesser goddesses."""},
    {"id": 47, "name": "Efreet",
     "lore": """A type of powerful spirit in Arabic
folklore that wields the power of fire.
It is said they will grant various boons
of magic to those who summon
them, but they also have violent
tempers and will not hesitate to
kill anyone who sparks their ire."""},
    {"id": 51, "name": "Titania",
     "lore": """The queen of the fairies and King
Oberon's wife. She is based on the
Roman goddess Diana and was later
imagined as a fairy.
She is famously recognized as
a queen in William Shakespeare's
\"A Midsummer Night's Dream.\""""},
    {"id": 52, "name": "Oberon",
     "lore": """The king of the fairies and the
husband of Titania.
He is quite old, but due to a curse
he received when he was young, he
remains small yet still beautiful.
He often flirts with human women
and has earned many a scolding
from his wife as a result."""},
    {"id": 53, "name": "Silky",
     "lore": """A house fairy of England and
Scotland.
A welcome spirit, she carries out
household chores while everyone
sleeps. It is said you can hear her
silk skirts rustle as she works.
However, she is not without a
dangerous side and will kill anyone
who tries to cause harm to the family
she protects."""},
    {"id": 54, "name": "Setanta",
     "lore": """A brave young man in
Celtic mythology.
After defeating a fierce guard dog,
he volunteered to take its place,
thus earning himself "Culann's Hound"
as a nickname."""},
    {"id": 55, "name": "Kelpie",
     "lore": """A fairy of Celtic folklore that lives by
the water and takes the appearance
of a horse.
They often drown those who attempt
to ride them, but if tamed, they can
be valuable mounts."""},
    {"id": 56, "name": "High Pixie",
     "lore": """A higher class of pixie, these
are the Seelie Court's more powerful
soldiers.
They are charged with guarding
the ruins and caves where other
pixies dwell."""},
    {"id": 57, "name": "Jack o'Lantern",
     "lore": """An Irish spirit typically found in
swamps, bogs, or marshes.
Said to be spirits of the dead,
Jack-o'-Lanterns appear as floating
flames and are known around the
world by various names such as
Will-o'-the-Wisp and Hitodama.
They are also said to come out at
night to startle travelers and make
them lose their way."""},
    {"id": 58, "name": "Jack Frost",
     "lore": """A frost spirit made from ice and snow
that appears during the winter and
melts away in the spring.
Do not be fooled by his cute
demeanor, however, for Jack Frost
is known to freeze people with his
cold breath, smiling all the while.
Some suggest that he originally
looked like an abominable snowman
but may have changed form to
appear more approachable and thus
more easily lure in his victims."""},
    {"id": 59, "name": "Pixie",
     "lore": """Small fairies found in southwestern
Britain known for their cheerful
nature and love of pranks.
Their physical appearance changes
from region to region, but their
personality is always playful and
mischievous. A common prank they
like to pull is causing humans to
wander in circles. However, they are
also known to help farmers from
time to time and are generally
considered good fairies."""},
    {"id": 60, "name": "Nahobeeho",
     "lore": """A Jack Frost who looks like a certain
Nahobino. Not content with being a
mere demon, he pushes himself to
his limits.
His blue hair and costume are
homemade, and he's said to be
proud of his divine craftsmanship.
He likes snowy mornings, and by
his own words, aims to create a
world of silver."""},
    {"id": 64, "name": "Queen Medb",
     "lore": """The queen of fairies in Celtic
mythology.
Some say she was the inspiration for
William Shakespeare's Queen Mab,
leading many to conclude that she
and the fairy queen Titania, Oberon's
wife, are one and the same. She was
known to give mead mixed with her
blood to her many consorts."""},
    {"id": 65, "name": "Succubus",
     "lore": """A female demon in popular European
folklore during the Middle Ages.
They are known to visit men in their
sleep and have sex with them. And
though they appear beautiful in the
dream, in reality, they are ugly old
hags."""},
    {"id": 66, "name": "Kaiwan",
     "lore": """A god in Assyrian mythology
associated with the planet Saturn.
He is usually grouped with another
god, Sakkut."""},
    {"id": 67, "name": "Lilim",
     "lore": """A demon in female form from
Judeo-Christian lore known to tempt
sleeping men and attack infants.
She is the daughter of the demoness
Lilith, who tempted Adam. Like her
mother, she drains men of their
essence."""},
    {"id": 68, "name": "Incubus",
     "lore": """A male demon in popular European
folklore during the Middle Ages, and
the male counterpart to the
succubus.
They are known to visit women in
their sleep and have sex with them.
The offspring born from these
incidents are said to later become
witches and wizards."""},
    {"id": 69, "name": "Mokoi",
     "lore": """A monster from Australian indigenous
folktales.
It lives in a jungle alongside owls.
Though it appears human, it has an
abnormally large head. It also lacks
a tongue and therefore cannot speak.
Myth tells that these creatures are
reincarnations of the "soul of the
shadow," and they are even said
to engage in intercourse with human
women from time to time as well
as eat children and fight humans."""},
    {"id": 70, "name": "Sandman",
     "lore": """A fairy from rural Germany rumored
to put people to sleep using the
magic sand he carried in his bag.
If a victim resisted, he would sit
on their eyelids to force them to sleep.
It has even been said that naughty
children who refused to go to sleep
would be punished by having their
eyes scooped out and taken away,
though this is speculated to be a
fabrication thought up by German
mothers."""},
    {"id": 72, "name": "Black Frost",
     "lore": """A Jack Frost that grew powerful
and evil.
They are the evolved form of the
fairly peaceful winter fairy and
mark the transformation from
small prankster into massively
powerful entity."""},
    {"id": 75, "name": "Nuwa (Normal)",
     "lore": """A goddess that appears in Chinese
mythology.
Recognized as one of three
sovereigns, she is said to have the
head of a human and body of a
serpent. As a demigod, she is also
known to be responsible for the
creation of humanity, having created
humans from mud. Legend says that
when one of the four pillars said to
hold up the world broke, she
repaired it. Fuxi, also of the three
sovereigns, is typically labeled as
either her brother or her husband
depending on what version of her
story is told."""},
    {"id": 76, "name": "Amon",
     "lore": """One of the 72 demons of Solomon's
"Ars Goetia."
He is the seventh spirit of Goetia
and the Grand Marquis of Hell.
Amon is depicted in several different
forms, sometimes appearing as a wolf
with a serpent's tail, and other times
appearing as having the head of an
owl, the torso of a wolf, and the tail of
a snake sometimes replacing his hind
legs altogether. It is said that he
bestows knowledge of the past and
the future. He is also incredibly loyal,
having led his army to assist Satan
when Satan rebelled against God."""},
    {"id": 77, "name": "Mara",
     "lore": """A Buddhist demon that represents
the fear of death.
Also known as "The Evil One,"
he sent his daughters to tempt
Buddha during his meditations."""},
    {"id": 78, "name": "Mephisto",
     "lore": """More accurately, Mephistopheles.
He is one of the Princes of Hell, and
his name means "he who loves not
the light."
He is commonly known as the
demon summoned by Georg Faust.
Other than Satan himself, he is the
most feared commander in Hell.
However, he despises having fallen
into Hell and hates any and all
humans who have been granted
salvation. He is rather knowledgeable
in the realms of astronomy,
astrology, and meteorology in
addition to being a skilled illusionist
who can manipulate all five senses."""},
    {"id": 79, "name": "Chi You",
     "lore": """A Chinese demon king often depicted
with a bull's head, six or eight arms,
and four eyes.
He invented many weapons and
commanded an invincible army.
Seeking control of the mortal world,
he fought with the Yellow Emperor
Huang Di. Though he was winning,
the Yellow Emperor ultimately
defeated him. Huang Di then had
Chi You's head buried thousands
of li apart from his body."""},
    {"id": 80, "name": "Surt",
     "lore": """A fire giant in Norse mythology.
He rules over Muspelheim, the realm
of fire, and brandishes a sword of fire
called Laevateinn. In Ragnarok, he
will set the world ablaze."""},
    {"id": 81, "name": "Beelzebub",
     "lore": """Lord of the Flies and the Prince of
Hell.
He is established as a high-ranking
demon in the Bible, and his multitude
of flies are said to carry souls down
to the abyss. It has been speculated
that he is a bastardization of the
Canaanite god Baal."""},
    {"id": 82, "name": "Arioch",
     "lore": """The fallen angel of Israel and the
demon of vengeance.
His name means "ferocious lion," and
he is said to aid in the vengeance
of those who seek his service.
During his time as an angel of God,
he was recognized as the guardian
angel of the Saint Enoch. It is said
that his name originally belonged
to one in either the Book of Genesis
or the Book of Daniel, only to become
associated with the demon thereafter."""},
    {"id": 83, "name": "Belial",
     "lore": """One of the 72 demons of the "Ars
Goetia" invoked by King Solomon.
He leads 50 legions of demons as
their chief and is said to appear before
his conjurer as two beautiful angels
in a chariot of fire. His name means
"worthless," and he is known to be
exceptionally cunning, having caused
the fall of Sodom and Gomorrah in
addition to persecuting Jesus Christ."""},
    {"id": 84, "name": "Abaddon",
     "lore": """The king of the abyss that appears in
the Book of Revelation of the New
Testament.
He controls locusts and plagues, and
leads the seventh order of demons
who are set to appear at the sounding
of the fifth trumpet on Judgment Day,
when it is said that he will bring a
horde of locusts to make the people
suffer. His name in Hebrew means
"destroyer" or "endless pit." It is
thought that his origins lie in
deification of the natural disasters
caused by locust swarms."""},
    {"id": 85, "name": "Moloch",
     "lore": """A Middle-Eastern Canaanite god of
fire.
Tradition states that a bronze statue
of a human with the head of a bull
would be placed at their altars as an
object of worship. It is said that the
hollow cavity of the statue would
first be heated with fire, then
children would be put inside of it as a
sacrifice. The Bible mentions him as a
cruel pagan god."""},
    {"id": 86, "name": "Belphegor",
     "lore": """An evil spirit who oversees the deadly
sin of Sloth. He excels at both
invention and discovery.
It is rumored that he may be
the disgraced form of Baal Peor,
the Syrian god of abundant crops."""},
    {"id": 87, "name": "King Frost",
     "lore": """TODO"""},
    {"id": 88, "name": "Mithras",
     "lore": """A sun deity who was worshiped in the
Roman Empire from the 1st to the 4th
century AD.
The rituals of the religion were
secretive, but it is believed they
entailed covering oneself in the blood
of sheep and bulls. He was said to be
reborn after death, inspiring
worshipers to hold a festival each
winter solstice."""},
    {"id": 89, "name": "Loki",
     "lore": """A malevolent god of Norse mythology.
Though not always driven by malice,
he can be capricious and is quite
cunning. Despite being a blood
brother to Odin, he was punished for
many of his wrong doings, including
the murder of Odin's child Baldur."""},
    {"id": 94, "name": "Huang Long",
     "lore": """One of the holy dragons of Chinese
lore, the Golden Dragon appears in
times of great fortune or joy.
His dominion over the earth extends
to the four gods Qing Long, Xuanwu,
Zhuque, and Baihu."""},
    {"id": 95, "name": "Quetzalcoatl",
     "lore": """An Aztec creator deity known as the
Feathered Serpent.
He is identified as the sun and is also
known as the god of wind and giver
of breath. He is said to have created
humans by sprinkling blood on the
bones of people from a previously
created world, and acts as the
guardian of their fertility and culture.
According to legend, the planet Venus
is actually Quetzalcoatl's heart."""},
    {"id": 96, "name": "Qing Long",
     "lore": """One of the Ssu-Ling, celestial
creatures in Chinese mythology.
It represents the east, the season of
spring, and the element of wood. It is
the noblest of the Ssu-Ling and dwells
in a palace at the bottom of the
ocean. In Feng Shui, placing water to
the east is known to guide its power
and is said to bring good fortune."""},
    {"id": 97, "name": "Xuanwu",
     "lore": """One of the Ssu-Ling, celestial
creatures in Chinese mythology.
It represents the north, the season
of winter, and the element of water.
Known to be a great warrior, it is said
to support the Earth from below."""},
    {"id": 98, "name": "Ananta",
     "lore": """The 1,000-headed serpent of Hindu
legend. Ananta is Sanskrit for
"infinite."
Vishnu slept atop him before
waking up to create the universe."""},
    {"id": 99, "name": "Vritra",
     "lore": """A ferocious giant dragon of Hindu
mythology. Its name means
"obstacle," and it's said to block the
rivers in the sky, bringing drought.
When Indra, god of thunder, defeats
him, the earth's rains will return.
However, Vritra will rise again the
following year. The battle between
the two is said to continue for
eternity."""},
    {"id": 100, "name": "Nyami Nyami",
     "lore": """Zambezi River god of the Tonga
and Lozi tribes of southern Africa.
He has the body of a snake and the
head of a fish or dragon. He is said to
protect people near the water and
provide them with food. He lived with
his wife, Kitapo, until the construction
of the Kariba Dam, which separated
them. The local inhabitants were also
forced to move to barren land. It is
said that the great floods that
occurred during the construction of
the dam were caused by the Nyami
Nyami, who was angered by these
events."""},
    {"id": 103, "name": "Yamata no Orochi",
     "lore": """A giant snake with eight heads that
the hero Susano-o defeated to save
Kushinada-Hime.
The legendary sword
Ame-no-Murakumo-no-Tsurugi,
also known as the Sword of Kusanagi,
is said to have emerged from its belly."""},
    {"id": 104, "name": "Naga Raja",
     "lore": """The king of the Naga, a half-man,
half-snake tribe in Hindu lore.
The dragon kings Nanda and
Takshaka of Buddhist myth fall into
this royal category."""},
    {"id": 105, "name": "Yurlungur",
     "lore": """In Oceanian folklore, he is a giant
copper python.
A being that transcends good and
evil, he governs the weather and is
considered a god of the harvest.
It's said his body is long enough to
reach the heavens. He is also called
the Rainbow Serpent because the
water in the well he calls home
shines like a rainbow."""},
    {"id": 106, "name": "Naga",
     "lore": """Half-snake, half-human, they are
divine beings in Hindu lore.
Worshiped as bringers of fertility, they
live in the bottoms of lakes and seas,
and enjoy singing and dancing
outside of battle."""},
    {"id": 107, "name": "Nozuchi",
     "lore": """Said to be the spirit of a serpent
that has lived in the mountains since
ancient times in the Nihon Shoki and
is also said to govern the earth's
veins.
The name Nozuchi comes from the
ancient Japanese word for "god of
the fields." It is said to live deep in
the mountains behind trees and in
thickets. It has a large mouth at the
end of its head, but no eyes or nose.
It is not evil, but rather violent all the
same. When it sees a human, it may
try to harm or even eat them."""},
    {"id": 108, "name": "Vouivre",
     "lore": """A female dragon with bat wings,
eagle legs, and a viper tail. Sometimes
depicted as a beautiful female spirit.
The secret of Vouivre's power is a
garnet jewel on her forehead, which
if lost or stolen, causes her to lose
all her magical powers and forces
her to obey the gem's owner. Some
believe the jewel is not actually
found in the forehead, but actually 
refers to her eyes."""},
    {"id": 111, "name": "Vasuki",
     "lore": """A giant serpent of Hindu lore.
It is said that gods and demons used
his body to churn the chaotic sea
of milk and create Amrita, or
immortality. Using Mt. Mandara as a
pole and his body wrapped around it
as a rope, the gods and demons took
turns pulling his body on either side,
moving Mt. Mandara around in the
sea. The strain from this caused him
to spew incredibly poisonous venom,
which was then safely swallowed by
Shiva before it could ruin Amrita."""},
    {"id": 112, "name": "Seth",
     "lore": """The Egyptian god of the desert,
chaos, and evil.
He murdered his brother Osiris and
tried to become chief god, but he was
later castrated by Osiris's son Horus."""},
    {"id": 113, "name": "Basilisk",
     "lore": """A dark dragon from Northern Africa
marked by wings and a crested
crown.
Its name means "king of snakes,"
and both its breath and gaze are
so toxic that they instantly kill any
human or animal unfortunate enough
to be subjected to them."""},
    {"id": 114, "name": "Aitvaras",
     "lore": """A fairy in Lithuanian mythology.
Indoors, it takes the form of a black
cat or a rooster. Outdoors, it takes
the form of a small dragon or a snake
with a burning tail. The Aitvaras
makes the home it inhabits rich by
stealing from its neighbors. It is said
that it typically demands an omelet
as compensation and is difficult to
chase away once it's settled into a
home. It can, however, be
exterminated by shining it with the
flame of a candle purified by the
church."""},
    {"id": 115, "name": "Hydra",
     "lore": """One of the monsters in Greek
mythology. It is usually depicted as
having nine heads, but some say that
it has as many as 100.
Its father is Typhon, Giant of the Wind,
and its mother is Echidna, Goddess
of the Snake. The Hydra has
incredible regenerative power; so
much so that when one of its heads
is cut off, two more will sprout from
the wound. It is also extremely
venomous, and simply inhaling its
breath is enough to kill. The slaying
of Hydra is listed as one of the 12
great Labors of Hercules."""},
    {"id": 116, "name": "Fafnir",
     "lore": """TODO"""},
    {"id": 117, "name": "Zhu Tun She",
     "lore": """A monstrous snake-like beast sighted
in China during the Song dynasty.
It appeared before soldiers-in-training
and tried to swallow humans, but was
defeated by a soldier with sorcerous
powers. A bizarre, hairy quadruped
about three feet long, it emerges from
a bamboo grove with a pig-like squeal.
Because its features defy taxonomic
classification, it is highly suspected
to be a creature wholly unknown."""},
    {"id": 118, "name": "Samael",
     "lore": """An enigmatic angel whose name bears
the unusual meaning "poison of God"
and who is commonly depicted as a
winged serpent.
Though an angel, he is often referred
to as the leader of daemons. It's been
suggested that he's a fallen angel, but
several descriptions in the Bible and
other sources refute this."""},
    {"id": 119, "name": "Barong",
     "lore": """Said to live in the forests of Bali,
it was a great mythical beast whom
the people sanctified and made their
guardian.
Now a symbol of good, it is fated
to fight Rangda, the avatar of evil,
for all eternity."""},
    {"id": 120, "name": "Anubis",
     "lore": """The jackal-headed god of the dead
and embalming from Egyptian myth.
He weighs the hearts of the dead to
determine their final destination. He is
also said to govern the technique of
mummification."""},
    {"id": 121, "name": "Makami",
     "lore": """A divine beast in Japanese
mythology.
It has been said to ward off evil and
disasters, especially thefts and fire,
and is commonly drawn on "ema,"
a type of Japanese amulet.
However, despite being known
primarily for protection, it has
also been rumored to eat people."""},
    {"id": 122, "name": "Xiezhai",
     "lore": """A sacred beast resembling a sheep in
Chinese legend.
Its eyes are said to have the power
to see through any lie. Often
appearing in the human world, it is
said to punish the wicked with the
power of its sharp horn."""},
    {"id": 126, "name": "Baihu",
     "lore": """One of the Ssu-Ling, celestial
creatures in Chinese mythology.
It represents the west, the season of
autumn, and the element of metal. It
is believed to be the king of all
beasts."""},
    {"id": 127, "name": "Chimera",
     "lore": """A monster that is part lion, part goat,
and part snake.
Originally a symbol representing
the seasons, it became a violent
monster when adopted into Greek
mythology. Its father is Typhon
and its mother Echidna."""},
    {"id": 128, "name": "Cironnup",
     "lore": """\"Fox\" in the Ainu language. Though
"sumari" is another word for fox,
"chironnupu" refers to "those who
we kill," and is said to be the general
word for small-to-medium-sized
animals.
In Ainu culture, it is also a divine
beast that alerts people to
forthcoming disasters by howling
loudly from the mountains."""},
    {"id": 129, "name": "Shiisaa",
     "lore": """A holy beast said to protect houses
from evil and grant them fortune.
Though it may look similar to Shinto
guardian dogs, it is actually modeled
after a lion. There are many stories
about it in Ryukyu lore."""},
    {"id": 130, "name": "Senri",
     "lore": """A yokai said to be born from the
incarnation of a long-lived wildcat. It
disguises itself as a beautiful woman
and collects vitality from human
men.
It is said to be the highest rank
possible for a beast's demonic
incarnation, similar to nekomata.
Some believe all beast-demons
gather spirits in the hopes of
becoming a Senri themselves."""},
    {"id": 131, "name": "Unicorn",
     "lore": """A white horse of Scottish legend,
featuring a spiral horn on its forehead.
This horn is said to make a panacea
for all manner of ailments, but it will
only open its heart to the purest of
maidens, allowing only them to
touch its body."""},
    {"id": 134, "name": "Cerberus",
     "lore": """The guardian hound of Hades in
Greek lore.
It traditionally has three heads and
a snake's tail. It was born from
Typhon, the Giant of Wind, and
Echidna, the Mother of Monsters.
It is also the older brother of Orthrus."""},
    {"id": 135, "name": "Orthrus",
     "lore": """The two-headed dog who protected
the Titan Geryon's red cattle in Greek
lore.
Despite his skill as a guard, Hercules
killed him in one blow while
performing one of his 12 great labors."""},
    {"id": 136, "name": "Loup Garou",
     "lore": """A type of werewolf originating in
France. It appears human during the
day but transforms into its beastly
form at night, when it has been
known to viciously attack humans.
They are said to have once been
ordinary human beings. However,
upon turning into a loup-garou, one
cannot regain their humanity ever
again."""},
    {"id": 137, "name": "Nekomata",
     "lore": """Incarnations of long-living cats in
Japanese mythology.
They can speak to humans and, 
depending on their power, can do
various things. Some can turn into 
humans, while others can have the
dead do their bidding."""},
    {"id": 138, "name": "Inugami",
     "lore": """Spirits of dogs said to possess
humans in Japanese folklore.
Those possessed enter a state of
"inu-tsuki" and go crazy. Onmyoji,
or Japanese sorcerers, summon
them to do their will.
It is often used as a curse to
humiliate people, and it is said that
this spirit is created by ending the
life of a living dog in accordance
with the art."""},
    {"id": 139, "name": "Orobas",
     "lore": """One of the 72 demons
of the "Ars Goetia."
He is said to appear as a human with
the head of a horse. He answers all
questions concerning past, present,
and future, and is both liked and
respected by sorcerers. According
to legend, he was often summoned
by sorcerers seeking to see through
lies or predict the future."""},
    {"id": 140, "name": "Cait Sith",
     "lore": """A fae beast from the Scottish
highlands whose kingdoms can be
found in tree hollows or abandoned
houses.
Dog-sized, they have white tufts of
hair on their chest, green, intelligent
eyes, and are even capable of
understanding the human language.
Though they usually stick to their
territory, some have been known to
live with humans as normal black
cats. They are generally peaceful,
but should a human treat one poorly,
they will forcibly take that human to
their kingdom."""},
    {"id": 141, "name": "Dormarth",
     "lore": """A canine demon of Celtic mythology.
Commanded by Gwyn, King of the
Afterlife, she is said to be a hound
with a red nose visible through even
the mountain mist. The meaning of
her name is uncertain and subject
to much speculation, but the most
common theory is "death's door,"
and she is thought to be the
gatekeeper of the afterlife
under Gwyn's reign."""},
    {"id": 142, "name": "Glasya Labolas",
     "lore": """One of the 72 demons of the
"Ars Goetia," sometimes referred
to as Caacrinolaas.
His form is described as a dog with
griffin-like wings, and he can impart
instant knowledge in all arts and
sciences. It is also said that he is
the author of bloodshed and murder,
excels at predicting the future, and
can make people invisible.
Some accounts suggest the demon
Nebiros uses him as a mount."""},
    {"id": 144, "name": "Bugs",
     "lore": """A type of goblin from Welsh folklore
that eats children who don't listen to
their parents.
They are said to look like humans 
covered head to toe with hair, and
are recognized as an iconic monster
that appears at nighttime.
They are often spoken of by mothers
wishing to discipline their children as
noted in the popular phrase, \"For
naughty kids who disobey, the Bugs
will come and surely prey.\""""},
    {"id": 145, "name": "Nue",
     "lore": """A legendary monster in Japanese
mythology. It has the head of a
monkey, the body of a tanuki, the
arms and legs of a tiger, and the tail
of a snake.
Due to its bizarre appearance, the
term "Nue" is sometimes used
to describe a person of unknown
origins. According to "The Tale of
the Heike," the Nue would come
to the emperor's palace every night
from 2 to 2:30 A.M., shrouded in
a dark cloud, where it would howl
in a horrific and terrifying manner.
However, the warrior Minamoto no
Yorimasa eventually shot it down
with his bow."""},
    {"id": 146, "name": "Bicorn",
     "lore": """An evil creature that looks like a horse
with two curved horns.
It is said to be the opposite of
a Chichevache, but theory speculates
that it is actually a mistranslation of
Re'em, a two-horned beast that
appears in the Old Testament."""},
    {"id": 147, "name": "Mothman",
     "lore": """A cryptid sighted in West Virginia from
the 1960s to the 1980s.
It has red, shining eyes and was
known for the finlike appendages
on both sides of its body. It has been
said to walk on two feet and fly
without moving these appendages.
It has a keen sense for blood which
allows it to easily track its prey.
Eyewitnesses say that a UFO was
sighted when Mothman appeared,
so many believe that it is actually
an alien."""},
    {"id": 148, "name": "Fenrir",
     "lore": """A monstrous wolf of Norse mythology.
Son of the evil god Loki, he is said to
swallow the god Odin at the world's
end.
He is bound with the magic rope
Gleipnir, but it is said that he
will be released from this bondage
on the apocalyptic day of Ragnarok
and stand against the gods."""},
    {"id": 149, "name": "Peallaidh",
     "lore": """TODO"""},
    {"id": 152, "name": "Hayataro",
     "lore": """The spirit of a monster-busting dog
that used to live at Kozen-ji.
Long ago, the villagers of Mitsuke
would offer one of their own girls
to a giant monkey yokai to prevent it
from ravaging the fields. A monk
passing by learned of this, and
that the yokai greatly feared Hayataro.
The monk then rushed off and found 
Hayataro at Kozen-ji. Hayataro was
offered in place of a village girl, where
he then defeated the yokai, but was
mortally wounded in the epic battle.
The loyal dog traveled back to
Kozen-ji, where he died shortly
after reuniting with his master."""},
    {"id": 155, "name": "Flaemis",
     "lore": """A fire elemental; one of the four
elements in energy form.
It is said to be composed of both
dry and heat essences.
The ancient Greek concepts of
the four basic elements significantly
influenced early astrology."""},
    {"id": 156, "name": "Aquans",
     "lore": """A water elemental; one of the four
elements in energy form.
According to Aristotle, it is composed 
of both moist and cold essences."""},
    {"id": 157, "name": "Aeros",
     "lore": """A wind elemental; one of the four
elements in energy form.
It is said to be a fusion of moist 
and heat essences, forming
the basis for an exponential energy
increase."""},
    {"id": 158, "name": "Erthys",
     "lore": """An earth elemental; one of the four
elements in energy form.
It is said to be composed of dry
and cold essences, which are
known to be the basic components
of destruction."""},
    {"id": 171, "name": "Black Ooze",
     "lore": """An amoeba-like monster that attacks
and eats people.
Supposedly, it is actually a demon
that failed to take form and now
roams in search of Magatsuhi.
It is said that when a Slime's ability
to absorb Magatsuhi goes out
of control, it transforms into
a Black Ooze."""},
    {"id": 172, "name": "Legion",
     "lore": """A demon or horde of demons quoted
as saying, "For we are many" in the
New Testament.
The name comes from the Roman
military term for an army unit of
3,000 to 6,000 men."""},
    {"id": 173, "name": "Slime",
     "lore": """"A gel-like monster. It is said to be the
byproduct of a failed summoning.
Devoid of its original powers, it is
trapped in an incomplete gel form.
There are several theories of when the
slime first was recorded as a monster.
They tend to collect shiny objects."""},
    {"id": 174, "name": "Mad Gasser",
     "lore": """A mysterious figure that spreads an
unknown poisonous gas around.
He wears all black and is said to be a
tall man. The gas he uses has a sweet
smell, but inhaling it will cause intense
headaches and vomiting. He returns
when people begin to forget his
existence, though he is rarely sighted."""},
    {"id": 175, "name": "Turbo Granny",
     "lore": """The ghost of an old lady who runs
on all fours at blazing speeds near
Mt. Rokko.
Should you manage to catch a
glimpse of her back as she races by,
you will likely see a piece of paper
posted on her back that reads
"Turbo." She is not a dangerous
ghost, but her love for speed is
insatiable. Similar ghosts include the
"Dash Hag" of the Shuto Expressway
and the "100 km/h Granny" of
Hokkaido."""},
    {"id": 178, "name": "Shiva",
     "lore": """The great god who governs the
destruction and creation of the world.
He is the most worshiped god in
Hinduism alongside Vishnu.
It is said that he purifies the world
through destruction only to rebuild it
anew, and though he casts terrifying
destruction against the demons, he
also blesses his followers. Shiva
has been depicted in many ways, but 
the most common is for him to have
four hands, one face, and three eyes.
He wields a trishula, or trident, and
his third eye is said to emit a ray of
light that destroys all it touches."""},
    {"id": 179, "name": "Mot",
     "lore": """The Canaanite god of death.
Every year he attempts to kill Baal,
the god of fertility, only to see him
raised from the dead with the help
of Baal's sister, Anat."""},
    {"id": 180, "name": "Zaou Gongen",
     "lore": """Repeller of evil found at Kinpusen
by En-no-Ozunu.
Believed to be a fusion of Buddha,
Guanyin, and Maitreya, he is a god
who originated from Japan, rather
than the Buddhavacana."""},
    {"id": 181, "name": "Asura",
     "lore": """A violent group of demons in Hindu
lore.
They were very powerful and
caused the gods great trouble. They
are a fiercely strict group and attack
anyone who runs counter to their
ideals. They were originally gods of
light worshiped in Persia. The
Zoroastrian god Ahura Mazda was
one of them."""},
    {"id": 182, "name": "Chernobog",
     "lore": """The god of night, evil, and death in
Slavic lore. His name means "black
god."
Like many other gods of the dead,
he is said to live below the earth.
His counterpart is Belobog,
the "white god." Despite being feared,
he was also worshiped. The curse,
"May the black god end you," is still
used in Ukraine to this day."""},
    {"id": 183, "name": "Dionysos",
     "lore": """The Greek god of wine and theater.
He had two births.
Myth tells that Zeus took the
premature Dionysus from his dying
mother, Semele, and allowed him
to mature inside his thigh
so that the underdeveloped god
might have a proper birth."""},
    {"id": 188, "name": "Danu",
     "lore": """The Sumerian goddess of fertility.
Her name means "Lady of Heaven,"
and she is often viewed as one and
the same with Aphrodite, Ishtar, and
Venus. She is also a goddess of
warfare, and it is said that even male
gods feared her great power."""},
    {"id": 189, "name": "Inanna",
     "lore": """TODO"""},
    {"id": 190, "name": "Kali",
     "lore": """The Black One, a symbol of death
and destruction.
She is said to be another face of
Parvati, Shiva's consort. Wearing a
necklace of human heads, she wields
numerous bloody swords, one for
each of her many arms. It is said that
when Durga, another form of Parvati,
was fighting the Asuras, she
summoned Kali and defeated
the Asura army in an instant."""},
    {"id": 191, "name": "Cybele",
     "lore": """Mother goddess of nature.
A temple for her was created atop a
mountain in Phrygia, now modern-
day Turkey, where she was
worshiped. She ruled over beasts and
was said to be served by lions. She
later became a goddess passionately
worshiped in Rome."""},
    {"id": 192, "name": "Skadi",
     "lore": """TODO"""},
    {"id": 193, "name": "Isis",
     "lore": """The mother goddess of Egypt.
She is wife and sister to Osiris,
god of the underworld.
Known for her powerful magic,
she could perform miracles such as
raising her husband from the dead.
As the patron goddess of the dead,
her image can be found at many
burial sites."""},
    {"id": 194, "name": "Kikuri Hime",
     "lore": """The goddess of Shirayama, also
called Shirayama-Hime, and the
deification of a maiden who relayed
Izanami's words.
She once mediated between Izanagi
and Izanami during their confrontation
in Yomi, the land of the dead. Since
she is the goddess of love and
marriage, she was thought to have
been named for "kukuri," meaning
\"to bring people together.\""""},
    {"id": 195, "name": "Hariti",
     "lore": """A Buddhist goddess also known
as Kishimojin.
She was originally an evil devil who
ate children, but when Buddha hid
the most beloved of her 500 children,
she was stricken with sorrow. Having
been taught the pain of losing a child,
she then became a good god and
started eating pomegranates instead
of children."""},
    {"id": 197, "name": "Nuwa (Snake)",
     "lore": """A goddess that appears in Chinese
mythology.
Recognized as one of three
sovereigns, she is said to have the
head of a human and body of a
serpent. As a demigod, she is also
known to be responsible for the
creation of humanity, having created
humans from mud. Legend says that
when one of the four pillars said to
hold up the world broke, she
repaired it. Fuxi, also of the three
sovereigns, is typically labeled as
either her brother or her husband
depending on what version of her
story is told.
She takes this serpentine form when
unleashing a portion of her power,
though she is capable of far more."""},
    {"id": 198, "name": "Alilat",
     "lore": """An Arabian mother goddess,
also known as Al-Lat.
Invoked for a variety of purposes,
from good weather and protection
to vengeance and pestilence."""},
    {"id": 200, "name": "Thor",
     "lore": """The Norse god of thunder and fertility
whose strength is incomparable.
He is a heroic and honest god
worshiped mainly by farmers and
is primarily known for defeating
the giants. He wields Mjolnir,
a hammer that returns to its owner
after being thrown. He and
the World Serpent, Jormungandr,
are fated to kill each other at
Ragnarok."""},
    {"id": 201, "name": "Futsunushi",
     "lore": """The Nihonshoki sword deity who
pacified Ashihara-no-Nakatsukuni.
His name comes from "futsu," the
fashion in which things are cut, and
"nushi," a term meaning, \"nature as a
god.\""""},
    {"id": 202, "name": "Attis",
     "lore": """A Phrygian god who symbolizes life,
death, and revival.
He rejected Cybele's love and was
driven mad, dying shortly after
castrating himself. Cybele then
resurrected him."""},
    {"id": 203, "name": "Bishamonten",
     "lore": """The strongest of the Four Heavenly
Kings, also known as Tamonten, and
in Buddhist mythology, Vaishravana.
He protects the North and is
recognized as the god of war.
Similarly to his fellow kings, he is
often depicted as a fierce warrior clad
in armor and wielding a great spear.
Bishamonten is also well known as a
bringer of fortune, being one of the
Shichi Fukujin, the seven gods of
fortune."""},
    {"id": 204, "name": "Jikokuten",
     "lore": """Jikokuten, protector of the East, is
one of the Four Heavenly Kings in
Buddhist mythology.
He is also known as Dhritarashtra,
and similarly to his fellow kings,
is often depicted as a fierce warrior
clad in armor and wielding a sword.
As his name suggests, it is said that
he bestows serenity upon a country."""},
    {"id": 205, "name": "Koumokuten",
     "lore": """Koumokuten, protector of the West,
is one of the Four Heavenly Kings of
Buddhist mythology.
Similarly to his fellow kings, he is
often depicted as a fierce warrior
clad in armor and wielding a trident.
He is also known as Virupaksha and
is said to keep a close eye on the
world with his sharp gaze, preaching
to the people all the while."""},
    {"id": 206, "name": "Zouchouten",
     "lore": """Zouchouten, protector of the South,
is one of the Four Heavenly Kings in
Buddhist mythology.
Similarly to his fellow kings, he is
often depicted as a fierce warrior
clad in armor and wielding a long
sword, though he is sometimes
shown wielding a trident instead.
Also known as Virudhaka, he is god
of the five grains."""},
    {"id": 211, "name": "Arahabaki",
     "lore": """A major deity in ancient Japanese
mythology. Clay dolls were often
sculpted in its image.
However, because this god was
known to be worshiped by a rebel,
the dolls later came to be considered
symbols of defiance."""},
    {"id": 212, "name": "Oyamatsumi",
     "lore": """One of the Kunitsukami in Japanese
mythology. He is the grandfather of
Susano-o's wife, Kushinada-Hime.
He is known as the god of the
mountains but is also considered
to be the god of water and rice fields
because he ruled over water sources
and harvests."""},
    {"id": 213, "name": "Kushinada Hime",
     "lore": """Kushinada-Hime is a goddess in
Japanese mythology.
When she was human, she was
saved from the eight-headed serpent
Yamato-no-Orochi by the storm god
Susano-o, whom she later wedded."""},
    {"id": 214, "name": "Sukuna Hikona",
     "lore": """One of the gods of Japanese lore.
Son of Kamimusubi, he was so small
he fell through her fingers at birth.
Though he would normally be
counted among the Amatsukami, he
became blood-brothers with
Okuninushi and is now considered a
Kunitsukami. After building Japan
with Okuninushi, he is said to have
returned to Tokoyo no Kuni, the land
of eternity."""},
    {"id": 215, "name": "Okuninushi",
     "lore": """A Kunitsu deity of Japanese
mythology that governs agriculture
and medicine.
Said to have built the country of
Izumo with Susano-o's daughter
Suseri-Hime. He is a peaceful god
who prefers not to fight."""},
    {"id": 216, "name": "Take Minakata",
     "lore": """A Japanese god of war, hunting, and
fertility.
He fought Take-Mikazuchi for control
of Japan and lost. He escaped to
Suwa but has been prohibited from
leaving ever since."""},
    {"id": 221, "name": "Ganesha",
     "lore": """The elephant-headed god in Hindu
mythology.
He was originally created
out of dirt by Pavarti to prevent
anyone from watching her bathe. It is
said that Shiva knocked his head off
but later replaced it with an
elephant's head."""},
    {"id": 222, "name": "Siegfried",
     "lore": """The name of the hero in the epic
German poem, the Nibelungenlied,
often seen as the same as Sigurd of
Norse folklore.
He was married to Kriemhild, the
princess of Burgundy, and is said to
have become wrapped up in a feud
between her and Brunhilde of
Austrasia, resulting in many attempts
on his life. The dragon Fafnir's blood
made him invincible, but a single leaf
on his back resulted in a weak spot,
which was later exploited by the
treacherous Hagen."""},
    {"id": 223, "name": "Valkyrie",
     "lore": """Daughters of Odin from Norse
mythology.
Their name means "choosers of
the slain." Armed with shining
armor and spears, they look for
brave warriors to take to Valhalla,
so that they may fight in Ragnarok."""},
    {"id": 224, "name": "Yoshitsune",
     "lore": """A Japanese general of the Genpei
War near the end of the Heian era
and start of the Kamakura era.
Also known as Ushiwakamaru, he is
said to have learned the art of war
from the Mt. Kurama Tengu. On
joining his half-brother Yoritomo's
army, he defeated the Taira one by
one, finishing them off at the battle
of Dan-no-ura. He was later pursued
by Yoritomo's army, only to kill
himself at Koromogawa."""},
    {"id": 225, "name": "Neko Shogun",
     "lore": """The god of prophecy in Taoist religion.
It is said to have the head of a cat and
the body of a human, and its shrine
was located in Annam, which is
present-day Vietnam. The shrine was
meant for Mao Shangshu, a 14-15th
century general who conquered
Vietnam. However, because the name
"Mao" is similar to the Chinese word
for cat, the temple was effectively
misnamed, and he was reborn as a
different god. It should also be noted
that there is a similar story about the
god of sailing known as \"Tetsu Neko
Shogun.\""""},
    {"id": 226, "name": "Nezha Taizi",
     "lore": """A protection deity of Chinese lore.
Sometimes said to take the form of
an ageless young man, he was
granted his trusty weapon Qiankun
Quan (Universe Ring) and his
trademark Hun Tian Ling (Red
Armillary Sash) upon birth. He later
committed suicide as atonement for
killing the Dragon King, but was
brought back to life with lotus roots.
In "Journey to the West," he fought
an intense battle with Sun Wukong."""},
    {"id": 227, "name": "Masakado",
     "lore": """A general who rebelled against the
Imperial Court in the mid-Heian
period: Taira no Masakado.
He succeeded in ruling Kanto and
declared himself emperor, but was
later defeated by Fujiwara no Hidesato
and Taira no Sadamori. After death,
he was enshrined as a vengeful spirit,
but was later viewed as a hero and
became revered as a guardian deity
of the Kanto region, where he has
remained to this day."""},
    {"id": 231, "name": "Mada",
     "lore": """A giant Asura in Hinduism whose
name means "the intoxicator."
It is said that the sage Chyavana
created it from fire. Mada has the
power to swallow its enemies, and
even the deity Indra has been said to
surrender to its power."""},
    {"id": 232, "name": "Girimekhala",
     "lore": """A giant elephant monster of
Sri Lankan mythology.
It is typically portrayed as being
ridden by Mara, the Evil One.
Whoever looks into its evil eye is said
to be met with great misfortune."""},
    {"id": 233, "name": "Pazuzu",
     "lore": """A demon from Sumerian civilization,
he governs the southwestern wind.
He has the face of a lion, the body
of a human, the wings of a bird,
the talons of an eagle, the tail of
a scorpion, and a curved horn
protruding from his forehead.
It is said that the wind he blew
from the Persian Gulf spread
disease throughout the land."""},
    {"id": 234, "name": "Mishaguji",
     "lore": """An indigenous god of the Shinano
region from before the forces of
Yamato occupied the land.
Said to be born from the belief that
divine spirits dwelled in rocks and
stones."""},
    {"id": 235, "name": "Baphomet",
     "lore": """An idol commonly worshiped
by the Knights Templar.
A demon with the head of a goat,
this figure later became the idol of
worship for witches as well."""},
    {"id": 236, "name": "Lahmu",
     "lore": """A god that appears in Babylonian
mythology.
Born from Apsu and Tiamat, he and
his sister, Lahamu, gave birth to
Anshar and Kishar. Lahmu is at times
depicted as a large serpent but has
also been illustrated as a man wearing
a red sash with six curls in his hair.
Regardless, he is always shown
alongside Lahamu, and it is thought
that together they represent the silt
in the sea where Apsu's fresh water
and Tiamat's sea water mix."""},
    {"id": 237, "name": "Saturnus",
     "lore": """A fertility god of Roman mythology,
associated with the primordial earth.
He is commonly identified with the
Greek god Cronus. Often referred to
as "Black Sun" by Chaldean
astronomers, linked to the low
position of the sun around the time
of the winter solstice. Also known as
the "Night Sun" and also the "King
of Death" living in the depths
of the underworld. It is said that
people prayed to Saturnus, the
winter sun, to call for a new spring,
and that custom became what we
now know as Christmas."""},
    {"id": 238, "name": "Tzitzimitl",
     "lore": """Aztec goddesses of night and fear.
They constantly attack the sun and
cause solar eclipses. They demand a
sacrifice once every 52 years."""},
    {"id": 240, "name": "Abdiel",
     "lore": """A high-ranking angel wholly devoted
to carrying out God's will. The name
Abdiel carries the meaning of "slave
to God," which supposedly originates
from the Arabic word for "slave."
Of all the angels who followed Lucifer,
Abdiel was the only one to reject the
temptation to rebel against God and
instead received God's praises for
returning to His side. Abdiel then led
the angels to fight against Lucifer."""},
    {"id": 241, "name": "Metatron",
     "lore": """One of the most important angels in
the hierarchy yet the most
mysterious.
He is the scribe and advocate
of heaven."""},
    {"id": 242, "name": "Michael",
     "lore": """One of the four major angels, his
name means "He who is like God."
He stands at the top of the angel
hierarchy and carries a divine
armament known to shatter any
blade."""},
    {"id": 243, "name": "Gabriel",
     "lore": """One of the four major angels. The
name Gabriel means "God is my
strength."
Acting as a messenger for God,
Gabriel is the one who informed
the virgin Mary of her pregnancy.
Though often depicted with a feminine
face, there are various interpretations
suggesting that Gabriel is not
androgynous but is in fact a woman."""},
    {"id": 244, "name": "Sraosha",
     "lore": """In Zoroastrian lore, Sraosha's duty is
to listen to humanity's cry for Ahura
Mazda.
It is also known to descend
after sunset to vanquish evil, and its
name literally means \"observance.\""""},
    {"id": 245, "name": "Raphael",
     "lore": """One of the four major angels. His
name means "healer."
He explains the history of the fallen
angels and the creation of Adam
and Eve."""},
    {"id": 246, "name": "Sandalphon",
     "lore": """The twin brother of Metatron.
An influential angel in Jewish
mythology, he governs the songs
of heaven, and his colossal size has
led many to believe that it would take
a human being 500 years to reach his
head."""},
    {"id": 247, "name": "Uriel",
     "lore": """One of the four major angels.
His name means "Flame of God,"
and he possesses knowledge of
all celestial phenomena. He is
also the first angel Satan met
after falling to Earth."""},
    {"id": 248, "name": "Camael",
     "lore": """The angel of God in Jewish
mythology. He rules over the angels
known as the Powers, and his name
Camael means "one who sees God."
He is also the commander of the
angels of destruction, punishment,
and death in addition to being the
ruler of Mars."""},
    {"id": 249, "name": "Melchizedek",
     "lore": """A Christian Gnostic angel said to be
the "savior of angels."
In the Bible, he is referred to as
"Melchizedek, king of Salem." One
account names his mother as the
virgin Sofonim. He is associated
with bread and wine, and known
as the head of the angels of
peace."""},
    {"id": 250, "name": "Mastema",
     "lore": """An angel who persecutes evil in
Hebrew lore. His role is to deliver
punishment on behalf of God.
He is said to be permitted by God
to tempt humans and test their faith,
and even has demons as his servants,
at the behest of God. The Zadokite
Fragments and the Dead Sea Scrolls
describe him as the angel of woe,
the father of all evil, and a flatterer
of God."""},
    {"id": 251, "name": "Armaiti",
     "lore": """An archangel worshiped in
Zoroastrianism, and one of the
Amesha Spenta.
She is the daughter of the head god
Ahura Mazda, and an angel who
oversees the earth and provides
pasture for livestock. Armaiti is
roughly translated as "devotion,"
and she is the personification of piety.
It is said that she is heartbroken when
sinful humans walk on her path, and
rejoices when those who follow the
laws of heaven feed their livestock
and birth pious and virtuous children."""},
    {"id": 254, "name": "Throne",
     "lore": """The third of the nine orders of angels.
Their Hebrew name, Ophan, carries
the meaning of "wheel."
They are the highest ranking angels
to carry a material body and are
tasked with carrying the seat of God."""},
    {"id": 255, "name": "Dominion",
     "lore": """The fourth of the nine orders of
angels. Their name carries the
meaning of "governance," and it is
their duty to oversee the other angels.
It is said that their work is the
embodiment of God's will, and that
they wish for this governance to
spread throughout the cosmos."""},
    {"id": 256, "name": "Power",
     "lore": """The sixth of the nine orders of angels.
Their name carries the meaning of
"power of God."
As their duty is to protect the souls of
humans, they are constantly on patrol
to guard against demon attacks.
It is said that more than a few fall
because they are in a position to be
easily tempted by demons, and many
now-fallen angels are said to have
originally been Powers themselves."""},
    {"id": 257, "name": "Principality",
     "lore": """The seventh of the nine orders
of angels.
They are charged with overseeing the
welfare of countries and civilizations."""},
    {"id": 258, "name": "Archangel",
     "lore": """Eighth of the nine orders of angels.
They are responsible for ministering
to humans and delivering messages.
As warriors of the heavens, they lead
the armies of heaven against the
forces of darkness. Archangels were
once considered the highest rank of
angels, but were placed eighth in the
medieval angelic hierarchy."""},
    {"id": 259, "name": "Angel",
     "lore": """Ninth of the nine orders of angels.
They are closest in nature to humans.
They watch over individuals and
offer warning to those who stray
from the path."""},
    {"id": 260, "name": "Cherub",
     "lore": """A senior angel in the angelic
hierarchy, ranked second in the
order of angels.
They are represented by four wings
and four faces, and carry the throne
of God or drive His chariot. In the
Bible, they are known as the
gatekeepers of the Garden of Eden,
where they are said to guard the
tree of life with flaming swords."""},
    {"id": 264, "name": "Abdiel (Fallen)",
     "lore": """A high-ranking angel wholly devoted
to carrying out God's will. The name
Abdiel carries the meaning of "slave
to God," which supposedly originates
from the Arabic word for "slave."
Of the angels who followed Lucifer,
Abdiel was the only one to reject the
temptation to rebel against God,
and instead received God's praises
for returning to His side.
As God's order threatened to crumble,
Abdiel took this form after resolving to
protect that order, and fell to darkness
to obtain power greater than that of
the angels."""},
    {"id": 265, "name": "Adramelech",
     "lore": """Chancellor of Hell and supervisor
of Satan's wardrobe. He has the body
of a mule, though he may also
sometimes appear as a peacock.
He was worshiped by the Assyrians,
who occasionally offered him
children as sacrifice."""},
    {"id": 266, "name": "Flauros",
     "lore": """One of the 72 demons
of the "Ars Goetia."
He appears as a leopard and can see
into both the past and the future.
He can also control fire, which he
uses to burn his adversaries to death."""},
    {"id": 267, "name": "Nebiros",
     "lore": """The general of Hell. He keeps watch
over other demons.
As one of Hell's greatest
necromancers, he can control
souls and corpses."""},
    {"id": 268, "name": "Berith",
     "lore": """One of the 72 demons
of the "Ars Goetia."
Known as the Duke of Hell,
he rides a gigantic horse and
burns those without manners."""},
    {"id": 269, "name": "Ose",
     "lore": """One of the 72 demons
of the "Ars Goetia."
Appearing as half-man and half-beast,
it is said that he can change his form
according to the desires of the one
who summons him, though not for
very long."""},
    {"id": 270, "name": "Eligor",
     "lore": """One of the 72 demons
of the "Ars Goetia."
He takes the appearance of a knight
and has the power to see things to
come. He also possesses great
knowledge of many wars."""},
    {"id": 271, "name": "Forneus",
     "lore": """One of the 72 demons
of the "Ars Goetia."
He appears as a great sea monster
and is skilled in many languages in
addition to being a master of rhetoric."""},
    {"id": 272, "name": "Andras",
     "lore": """One of the 72 demons
of the "Ars Goetia."
The great Marquis of Hell, he appears
where there is battle to stoke the
hatred within soldiers. He helps
defeat the enemies of those who
summon him."""},
    {"id": 273, "name": "Decarabia",
     "lore": """One of the 72 demons
of the "Ars Goetia."
He comes in the shape of a star
and has vast knowledge of herbs
and jewels. He can also control
birds at will."""},
    {"id": 274, "name": "Halphas",
     "lore": """One of the 72 demons
of the "Ars Goetia."
He is called the Count of Death
and Destruction, and appears as a
jet-black dove with blood-red eyes.
He is a craftsman and builds towers
full of weapons."""},
    {"id": 275, "name": "Azazel",
     "lore": """A leader of the Grigori, a group of
angels who descended to earth to
educate humans. He is said to have
committed acts of defiance against
God, such as being attracted to
beautiful human daughters on earth
and taking them as wives, and giving
humans various truths of forbidden
knowledge. Azazel imparted
knowledge of armors, ornaments,
and makeup, teaching men to fight
and struggle and women to dress up
and seduce men."""},
    {"id": 278, "name": "Garuda",
     "lore": """A divine bird-man in Hindu mythology.
He hunts Nagas as a result of a
dispute between the two creatures'
mothers. According to legend, he
once fought with the gods, and was
even granted immortality in exchange
for becoming Vishnu's carrier."""},
    {"id": 279, "name": "Zhuque",
     "lore": """One of the Ssu-Ling, celestial
creatures in Chinese mythology.
It represents the south, the season of
summer, and the element of fire. It is
said to resemble a quail in
appearance and have a beautiful
chirping voice."""},
    {"id": 280, "name": "Yatagarasu",
     "lore": """A divine creature in Japanese
mythology, they are three-legged
ravens that the goddess Amaterasu
sent to help humans.
It is said that they helped Emperor
Jinmu claim victory, and, despite
their divine standing, those who are
unworthy have been known to go mad
after looking them directly in the eye."""},
    {"id": 281, "name": "Jatayu",
     "lore": """The Hindu king of birds.
In the Ramayana, he fought bravely
against Ravana in an attempt to save
Sita, the wife of Rama, the seventh
avatar of Vishnu. However, he was
unfortunately defeated."""},
    {"id": 282, "name": "Feng Huang",
     "lore": """A legendary bird in East Asia, said to
appear only in times of peace. It is
the ruler of all birds. When it dies,
birds across the land chirp with
sadness."""},
    {"id": 283, "name": "Thunderbird",
     "lore": """A revered bird of Native American
mythology said to live atop
cloud-shrouded peaks.
It resembles an eagle, and its
wingbeats create mighty
thunderclaps. Some legends say its
eyes can unleash lightning, and other
accounts say it can carry an entire
lake on its back or even swallow an
entire whale whole."""},
    {"id": 287, "name": "Anzu",
     "lore": """An evil deity of Mesopotamian
folklore with an eagle's body
and lion's head.
While the god Enlil purified himself,
Anzu stole the Tablet of Destinies
from him in an attempt to become
the chief god."""},
    {"id": 288, "name": "Zhen",
     "lore": """A bird in Chinese mythology said to
have poison in its feathers because
it eats poisonous snakes.
Dipping a feather into wine will turn
it into a deadly poison, able to kill
anyone with a single drop."""},
    {"id": 289, "name": "Muu Shuwuu",
     "lore": """Meaning "evil bird," it is the ghost
of a young girl who died without
knowing love in Buryat folklore.
She seduces travelers, only to crack
their heads open and suck out their
brains with her beak."""},
    {"id": 290, "name": "Onmoraki",
     "lore": """A Japanese monster that takes the
form of a bird with the face of a man.
It produces a sickening chirp and
spits a wicked flame.
Its true identity is a corpse that hasn't
had a proper memorial service, and it
is said to appear before monks who
neglect their duties."""},
    {"id": 291, "name": "Gurulu",
     "lore": """A demon that takes the shape of a
giant bird in Sri Lankan mythology.
Also known as "Gurulu Yaksha."
It is believed to be a derivation
of Garuda, the spirit bird of Indian
mythology, which is in ideological
opposition to its place in Sri Lankan
mythology, in which it is interpreted
as a demon."""},
    {"id": 295, "name": "Cleopatra",
     "lore": """More specifically, Cleopatra VII. Her
name means "glory of the father" in
Greek.
She is known as one of the greatest
beauties ever to live, having charmed
many with her musical voice and
conversation skills. It is said that
all of history would have unfolded
differently had even her nose been
longer or shorter."""},
    {"id": 296, "name": "Rangda",
     "lore": """A wicked witch and the symbol of evil
in Balinese Hinduism. When women
who used magic held a grudge or
went down the path of evil, they
became this dreadful creature.
She spreads plagues, causes natural
disasters, curses people, and even
uses evil spirits to do her bidding.
The holy beast Barong that
symbolizes good is her eternal rival.
Even if defeated, she will come back
to life, and their battle will have no
end."""},
    {"id": 297, "name": "Dakini",
     "lore": """Hindu deities of passion and relations.
They are Kali's attendants.
They eat human flesh and gather
at graveyards and crematories
each night.
Their name means "sky dancer,"
and they are said to dance
through the sky with skulls as
blood-filled cups in their hands."""},
    {"id": 298, "name": "Atropos",
     "lore": """One of the three Moirae Sisters in
Greek mythology. 
She cuts the life threads of those
whose time has come."""},
    {"id": 299, "name": "Yakshini",
     "lore": """Semi-divine beings in Hindu
mythology.
Though they were once worshiped
by the Dravidians as goddesses of
the harvest, they became interpreted
as demons with the spread of
Hinduism and the two clashing
ideologies. They are depicted as
naked women with voluptuous
bodies."""},
    {"id": 300, "name": "Lachesis",
     "lore": """One of the three Moirae Sisters in
Greek mythology. 
She is the apportioner, measuring the
thread which determines each
person's life span."""},
    {"id": 301, "name": "Clotho",
     "lore": """One of the three Moirae Sisters in
Greek mythology. 
She is the spinner of the threads of
fate."""},
    {"id": 302, "name": "Manananggal",
     "lore": """A witch whose lore originated
in the Philippines.
It masquerades as a beautiful woman
during the day but transforms into a
blood-sucking monster at night. It
has the ability to separate its upper
and lower body, and can sprout bat
wings from its back to fly in search of
humans to suck their blood. It is said
that the Manananggal preys on
unborn fetuses in particular, using its
proboscis-like tongue to open the
wombs of pregnant women, wherein
it will suck the fetus's blood, or
devour it outright."""},
    {"id": 303, "name": "Lamia",
     "lore": """Half-woman, half-snake creatures that
appear in Greek mythology and are
said to reside in Libya.
They supposedly favor the blood of
children and young men.
Originally a beautiful Libyan queen
loved by Zeus, she was killed
by the goddess Hera, who was
jealous of her children.
In her madness, she is said
to have turned into a monster
that attacks and eats people."""},
    {"id": 304, "name": "Mermaid",
     "lore": """Half-woman, half-fish, inhabitant of
the ocean. Males are called mermen.
Mermaids are regarded as ill omens
by many fishermen, often foretelling
severe storms or poor catches.
Legend says they use their voices
to charm men, causing them to
crash their ships."""},
    {"id": 305, "name": "Leanan Sidhe",
     "lore": """A beautiful fairy of Irish lore that
yearns for the love of a human man.
She drains the life of her lovers in
return for granting them artistic
inspiration."""},
    {"id": 310, "name": "Ongyo-Ki",
     "lore": """One of the four oni controlled by
Fujiwara no Chikata, who ruled Iga
and Ise during the Heian Period.
By suppressing its aura, thereby
preventing others from sensing its
presence, it can effectively ambush
its enemies. Oni have been said to act
as liaisons between humans and gods,
and the Fudoki holds many records of
such exchanges in this region."""},
    {"id": 311, "name": "Shiki-Ouji",
     "lore": """A powerful creature often summoned
by Japanese sorcerers called
onmyoji.
They are used both to hurt and to
heal, but their true nature is said
to be very violent."""},
    {"id": 312, "name": "Sui-Ki",
     "lore": """One of the four oni controlled by
Fujiwara no Chikata, it can cause
floods with the swing of its arms.
In the Taiheiki, a brave courtier
named Ki no Tomo-o expelled
the oni by sending them an elegantly
phrased threat in poetic form."""},
    {"id": 313, "name": "Fuu-Ki",
     "lore": """One of the four oni controlled by
Fujiwara no Chikata, it sends
hurricanes to blow away its enemies.
Some say that Fuu-Ki is the original
ninja."""},
    {"id": 314, "name": "Kin-Ki",
     "lore": """One of the four oni controlled by
Fujiwara no Chikata, its body is so
hard that no weapons can penetrate
It and its comrades fell into hell
through holes that can still be found
in Mie Prefecture, Japan (the
modern-day Iga Province)."""},
    {"id": 315, "name": "Azumi",
     "lore": """A water deity of the Azumi, a
Japanese seafaring tribe. As such,
it can freely control water.
The three gods born from Izanagi after
he returned from Yomi are said to be
the Azumi tribe's ancestors."""},
    {"id": 316, "name": "IpponDatara",
     "lore": """A monster with one eye and one leg,
said to live deep in the mountains of
Kumano, Japan.
A single footprint measuring
30 cm has been sighted in the
snowy mountains."""},
    {"id": 317, "name": "Daemon",
     "lore": """TODO"""},
    {"id": 318, "name": "Oni",
     "lore": """A common demon in Japanese
mythology. This terrifying and
powerful creature is known to raid
human villages for food, riches, and
women.
It is characterized by red skin,
horns on its head, long claws,
and sharp fangs."""},
    {"id": 319, "name": "Karasu Tengu",
     "lore": """A member of the tengu race.
They do not have the long nose that
usually represents the tengu, but, as
the name "karasu" (crow) suggests,
they are said to have a sharp beak
similar to that of a crow. They harbor
an evil nature, seeking to corrupt
people by haunting them."""},
    {"id": 322, "name": "Hecatoncheires",
     "lore": """Giants born from Uranus and Gaia in
Greek mythology. The name means
"those with a hundred arms."
During the war of the Titans, Zeus
freed them from the underworld to
help him obtain victory."""},
    {"id": 323, "name": "Loa",
     "lore": """A group of divinities worshiped in
voodoo religion.
Of the many hidden entities
mentioned in religious doctrines,
the ones that influence human
activities in the earthly realm
are known by this name. It is said
that those aligned with shadow also
possess powerful dark magic."""},
    {"id": 324, "name": "Rakshasa",
     "lore": """Evil spirits that battle the gods in
Hindu lore. They also attack humans.
Their hideous appearance symbolizes
their evil nature, but they can also
change shape to fool humans.
They are also said to feed on
human corpses to encourage
slander and distrust."""},
    {"id": 325, "name": "Turudak",
     "lore": """An Indian deity that serves Yama, the
god of death. 
When Yama judges a dead soul to be
guilty, Turdak acts as the executioner
and drags that soul to hell."""},
    {"id": 326, "name": "Macabre",
     "lore": """An evil spirit appearing in medieval
oratorios as the grim reaper. 
It is truly Death itself, with the power
to lead humans to their demise in an
instant. It is depicted as a skeleton
with a black cloak and a sickle to reap
human souls in a single stroke. True
to its name, it dances the feared
Dance of Death, a reminder that all
worldly things must someday meet
their end."""},
    {"id": 327, "name": "Gremlin",
     "lore": """A mischievous sprite that enjoys
wreaking havoc on machines and
tools. It's said that during World War
II, Gremlins often were found when
examining plane failures.
Though rather troublesome
creatures, Gremlins have been
known to be quite useful at times
and are even said to have helped
Benjamin Franklin with his famous
kite experiment."""},
    {"id": 330, "name": "Kaya-no-Hime",
     "lore": """A goddess of grasses in Japanese
mythology.
The name "Kaya" refers to the grass
that was used to build traditional
grass-roof houses, highlighting its
importance to the people of ancient
Japan."""},
    {"id": 331, "name": "Tsuchigumo",
     "lore": """Monsters said to come from the
bastardization of certain clans of
Japan. The word carries the literal
meaning of "dirt spider."
Those who did not pledge allegiance
to the Imperial Court were called this
derogatory term because of their
short stature and spindly limbs.
As time passed, people may have
misinterpreted the name for a literal
meaning and made them into spiders,
or perhaps the manifestations of
grudges of those who were
persecuted by the Imperial Court."""},
    {"id": 332, "name": "Narcissus",
     "lore": """A young man of Greek lore.
He rejected the nymph Echo, who
faded to a whisper out of despair.
Cursed by Nemesis, he fell in love
with his own reflection and wasted
away, becoming the flower that now
bears his name."""},
    {"id": 333, "name": "Hua Po",
     "lore": """Tree spirits in Chinese mythology that
are born when three or more people
hang themselves from the same tree.
They take the form of a beautiful
woman in white clothing, however
they are much smaller in size than a
human. They cannot talk, though they
can chirp like birds."""},
    {"id": 334, "name": "Koropokkur",
     "lore": """Small human-like creatures that have
kind, calm personalities.
Once coexisting with the Ainu people
of Japan, there was a falling out at
some point, and they disappeared."""},
    {"id": 335, "name": "Sudama",
     "lore": """Earth spirits in Japanese mythology.
They are born from ancient trees
and boulders.
They are not evil but will transform
into humans or monsters to warn
people not to infiltrate their
mountains."""},
    {"id": 336, "name": "Kodama",
     "lore": """In Japanese mythology, they are the
spirits of plants. They are born from
trees that live 100 years.
It was once thought that the echoes
heard in valleys were actually from
Kodama replying."""},
    {"id": 337, "name": "Gogmagog",
     "lore": """A giant believed to have lived on the
island of Britain in prehistoric times.
His body was so huge that he could
destroy a sailing ship with a swing
of his arm. He repelled all who
invaded the island, but was defeated
by Brutus of Troy."""},
    {"id": 341, "name": "Pisaca",
     "lore": """A type of demon in Hindu mythology
that arises from the vices of men such
as criminals, drunkards and
adulterers.
Known to feast on the flesh of
corpses, it is said that it can possess
a human by entering through their
mouth, where it will plague them
until it is driven away through magic
or medicine. It is also said that
anyone who looks upon one directly
is guaranteed to die within nine
months."""},
    {"id": 342, "name": "Kumbhanda",
     "lore": """Demons of Buddhist origin, known for
draining the life energy of humans.
It is said that they often change shape
and take the form of a gourd. They
stand three meters tall, with red hair
and dark skin, and have the body of a
human but the head of a white horse.
They once served Rudra, but
according to Buddhist scriptures,
they now follow Zouchouten of the
Four Heavenly Kings."""},
    {"id": 343, "name": "Poltergeist",
     "lore": """A mischievous spirit known for
haunting houses. The name is
German in origin, and literally
means "noisy ghost."
It can do various things, from pulling
harmless pranks like making loud
noises and moving objects through
the air, to dangerous, destructive
acts, like starting fires and assaulting
people. Poltergeist incidents often
occur in homes with children or
teenagers, and one theory states
that the cause is a child's unstable
mentality."""},
    {"id": 344, "name": "Obariyon",
     "lore": """A "piggyback monster" of Japan that
jumps on the backs of those who
walk on wooded paths at night.
Its weight becomes progressively
heavier to the point of being nearly
unbearable, but it is said that it will
transform into gold coins if you can
carry it all the way back home."""},
    {"id": 345, "name": "Preta",
     "lore": """Known as "gaki" in Japanese, they
are ghoulish demons of Buddhist lore.
Greedy humans cast into the preta
realm become these. Their hunger is
unrelenting and their suffering
continues until they are reincarnated."""},
    {"id": 346, "name": "Kudlak",
     "lore": """An evil vampire who fights Kresnik,
a proxy of God.
It is said that all bad things, including
disease, poor harvests, and bad luck,
are all under Kudlak's purview.
He transforms into various animal
forms to fight with Kresnik, and his
other forms are always colored black."""},
    {"id": 350, "name": "Trumpeter",
     "lore": """Angels that sound their trumpets to
signify the coming of the apocalypse
ordained in the Book of Revelation.
It is said that the trumpets bring
plagues and disasters, turning the
earth into a land of death and
suffering."""},
    {"id": 351, "name": "Mother Harlot",
     "lore": """Reviled as the "Whore of Babylon" in
the Book of Revelation.
She defies God from atop a
scarlet-colored beast with seven
heads and ten horns, and carries a
golden cup brimming with
abominations and the filth of her
deeds."""},
    {"id": 352, "name": "Black Rider",
     "lore": """One of the Four Horsemen of the
Apocalypse spoken of in the Book of
Revelation.
He rides a black horse and carries
scales, indicating the terrible famine
he is to bring. He has also been given
the authority to end the lives of those
who are suffering."""},
    {"id": 353, "name": "Red Rider",
     "lore": """One of the Four Horsemen of the
Apocalypse spoken of in the Book of
Revelation.
He rides a red horse and carries a
greatsword. It is said that he has the
power to destroy peace and make
men slay one another."""},
    {"id": 354, "name": "White Rider",
     "lore": """One of the Four Horsemen of the
Apocalypse spoken of in the Book
of Revelation.
He rides a white horse and carries a
bow. Wears a resplendent crown
as a symbol of God's dominion over
Armageddon, and promises to bring
total victory."""},
    {"id": 355, "name": "Alice",
     "lore": """A mysterious spirit that takes the form
of a blonde girl. Despite her innocent
appearance, she possesses
immeasurable magical strength.
Some say she is the ghost of an
English girl who died a tragic death.
Others say she is merely an
apparition born from someone's
imagination."""},
    {"id": 356, "name": "Hell Biker",
     "lore": """A biker-turned-Fiend that claims to
come from Hell.
Armed with an intense hatred of
himself and the world, his reliance
solely on his own power turned him
into this abominable figure."""},
    {"id": 357, "name": "Daisoujou",
     "lore": """A monk who died while fasting for
the sake of humanity. Because of
his intense spiritual power, his body
continues to exist without rotting.
It is said that on the day of salvation,
he will appear in front of humankind
once again."""},
    {"id": 358, "name": "Pale Rider",
     "lore": """One of the Four Horsemen of the
Apocalypse spoken of in the Book
of Revelation.
He rides upon a sickly pale horse
and bears the name "Death." The
embodiment of Hell itself follows
behind him, eager to claim his victims.
Fittingly, he has been given authority
to mete out widespread death and
disease."""},
    {"id": 359, "name": "Matador",
     "lore": """A master sportsman who entertains
the audience at the cost of his own
peril; even one small slip-up can spell
certain death.
It is said that some of the men who
die in this cruel game remain in this
world as Fiends, bound by regret as
well as the thirst for the cheers and
excitement."""},
    {"id": 365, "name": "Tao (Goddess/Ueno)",
     "lore": """Once cherished as the Saint of
Bethel, Tao Isonokami was forced
to watch helplessly as a close friend
perished before her eyes.
It was then that the voice of a
higher being spoke unto her,
awakening the goddess power within.
Even after her divine transfiguration,
she appears to have retained her
memories. However, she has cast off
her former personality, and no longer
acts as she did as a human."""},
    {"id": 366, "name": "Yoko",
     "lore": """TODO"""},
    {"id": 370, "name": "Shujinkou Nahobino",
     "lore": """TODO"""},
    {"id": 381, "name": "Hare of Inaba",
     "lore": """Known in Japanese as "Inaba no
Shirousagi," it is a smart rabbit
written about in the Kojiki, worshiped
as a hare god.
Wanting to cross the sea from
Oki Island to the mainland, he had
sharks line up in a row and
crossed on them, under the guise of
helping to count them. Once he
crossed and revealed that he was
just using them as a bridge, the
sharks skinned him. He was healed
by a passing god."""},
    {"id": 385, "name": "Kinmamon",
     "lore": """Highest god of Ryukyu Shinto. He hails
from the eternal kingdom Nirai Kanai,
and protects the Ryukyu Islands.
There is a Yin and a Yang duality
to this deity, with Kiraikanaino
Kinmamon coming from the sky
and Ohokakerakuno Kinmamon
from the sea. He brings gifts of
wisdom, and appears before
people through women."""},
    {"id": 386, "name": "Onyankopon",
     "lore": """A sky god of the Ashanti people and
other tribes in West Africa. One of the
aliases of the supreme god Nyame,
said to mean "the all-knowing and
all-seeing."
The god of spiders who created all
things, he is said to be the god who
imparts joy and motivation to live,
and the one people look to in times
of hardship. At first, he lived near
humans, but when they struck the
roots of a yam with a pestle, he
migrated to the sky. Although far
removed from humans, he is not
considered unapproachable."""},
    {"id": 387, "name": "Amabie",
     "lore": """A Japanese yokai said to have
appeared in the Higo Province during
the Edo period. One day, it was
spotted as a glowing object in the sea,
and made a prophecy to those who
investigated it. The prophecy was that
for the next six years, there would be
a bountiful harvest, but also an
epidemic of disease. Once that time
came, it said, those who fell ill should
be shown a drawing of Amabie as
soon as possible to ward off the
sickness. Similar rumors were
recorded around this time for
amabiko, jinjahime, and kudan."""},
    {"id": 391, "name": "Lilith",
     "lore": """Said to have been Adam's first wife.
Refusing to obey him, she left Eden
and became a demon of the night.
Though there are several theories
regarding her disobedience, she is
often regarded as a symbol of
infidelity. Some theories suggest she
was originally the mother goddess
of Babylonia. In the Zohar, a Jewish
spiritual text, she is listed as
the first of four female demons;
seducer of men, killer of infants, and
first consort of Samael."""},
    {"id": 392, "name": "Agrat bat Mahlat",
     "lore": """Agrat bat Mahlat. One of the four
female demons in the Zohar, a
spiritual text of Jewish mystical
thought.
Her name means "Agrat, daughter
of Mahlat": said to be the child of
Mahlat, daughter of Ishmael, who
had a child with a desert demon
named Igrathiel. A queen of demons,
she is called "the demon who dances
on the roof" and is said to wander
the air with a horde of messengers
of destruction on Wednesday and
Sabbath eve. It is also said that men
sometimes begged Agrat for help,
seeking for her to share the night
with them."""},
    {"id": 393, "name": "Naamah",
     "lore": """One of the four female demons in
the Zohar, a spiritual text of Jewish
mystical thought. Her name means
"pleasure" in Hebrew.
She is the most carnal of the four
demons, and specializes in seduction.
She is said to have intercourse with
human men in their dreams and to
give birth to numerous evil spirits,
almost solely driven by her own
desires. Her beauty bewitches even
angels, and she birthed the demon
king Asmodeus with an angel named
Shomron. It is believed she was
originally a human female, sister of
Tubal-cain (a descendant of the Old
Testament's Cain), and only later was
she interpreted as a demon."""},
    {"id": 394, "name": "Eisheth Zenunim",
     "lore": """Eisheth Zenunim. One of the four
female demons in the Zohar, a
spiritual text of Jewish mystical
thought.
Said to be a princess of the Qlippoth,
a concept of evil power in the same
school of thought, she is the
embodiment of sin; seducing many
humans and leading them to their
destruction. It is said that when
people abuse words with mystical
power, those words are taken away
by the devil to create an evil world
of arrogance and vanity. From this
world, Eisheth appears to terrorize
humanity."""},
    {"id": 400, "name": "Yoko Hiromine",
     "lore": """TODO"""},
    {"id": 401, "name": "Tao Isonokami",
     "lore": """TODO"""},
    {"id": 402, "name": "Yuzuru Atsuta",
     "lore": """TODO"""},
    {"id": 403, "name": "Ichiro Dazai",
     "lore": """TODO"""},
    {"id": 1157, "name": "Yoko Hiromine (Da'at - Minato)",
     "lore": """TODO"""}
]


(DEMON_ID_MAP, DEMON_NAME_MAP) = make_maps_dict(DEMONS)
