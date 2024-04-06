class DocumentInfos:

    title = u'Camera robot follow'
    first_name = 'Amaël'
    last_name = 'Margelisch'
    author = f'{first_name} {last_name}'
    year = u'2024'
    month = u'Avril'
    seminary_title = u'Projet OCI'
    tutor = u"Cédric Donner"
    release = "(Version finale)"
    repository_url = "https://github.com/Amael-Margelisch/robot-camera-follow"

    @classmethod
    def date(cls):
        return cls.month + " " + cls.year

infos = DocumentInfos()