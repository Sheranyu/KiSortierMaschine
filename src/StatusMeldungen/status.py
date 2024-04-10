


from typing import Callable


class WarnStatus():
    MODEL_NICHT_GEWAEHLT = "Ein Model Typ Muss ausgewählt werden"
    PFAD_OR_MODELNAME_NICHT_GEWAHLT = "Model oder Pfad wurde nicht ausgewählt"
    CLASS_NAME_EMPTY = "Der Name der Klasse ist leer bitte vergebe einen Namen"
    PFAD_IS_EMPTY = "Es wurde kein Speicherort angeben"
    FORBIDDEN_TWO_VIDEO_REC = "Es dürfen keine 2 Aufnahmen gleichzeitig laufen!"
    TIMEOUT_WARN = "Zeitüberschreitung"
    
    

def check_and_warn(openbanner: Callable[[str], None],condition, warn_status) -> bool:
        if condition:
            openbanner(warn_status)
            return True
        return False
    
    
class TypeErrorMessages:
    DICT_IS_NO_STRING: str = "dictname muss ein String sein"


class MCRMeldungen:
    GEDREHT: str = "gedreht"
    SERVO_GEDREHT: str = "servo_gedreht"
    LED_UMGESCHALTET: str = "led_umgeschaltet"
