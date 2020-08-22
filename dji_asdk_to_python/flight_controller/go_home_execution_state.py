import enum


class GoHomeExecutionState(enum.Enum):
    """
    An enum used to identify the different stages of the go-home command.
        - NOT_EXECUTING: The aircraft is not executing a Go-Home command.
        - TURN_DIRECTION_TO_HOME_POINT: The aircraft is turning the heading direction to the home point.
        - GO_UP_TO_HEIGHT: The aircraft is going up to the height for go-home command.
        - AUTO_FLY_TO_HOME_POINT: The aircraft is flying horizontally to home point.
        - GO_DOWN_TO_GROUND: The aircraft is going down after arriving at the home point.
        - BRAKING: The aircraft is braking to avoid collision.
        - BYPASSING: The aircraft is bypassing over the obstacle.
        - COMPLETED: The go-home command is completed.
        - UNKNOWN: The go-home status is unknown.

    """

    NOT_EXECUTING = "NOT_EXECUTING"
    TURN_DIRECTION_TO_HOME_POINT = "TURN_DIRECTION_TO_HOME_POINT"
    GO_UP_TO_HEIGHT = "GO_UP_TO_HEIGHT"
    AUTO_FLY_TO_HOME_POINT = "AUTO_FLY_TO_HOME_POINT"
    GO_DOWN_TO_GROUND = "GO_DOWN_TO_GROUND"
    BRAKING = "BRAKING"
    BYPASSING = "BYPASSING"
    COMPLETED = "COMPLETED"
    UNKNOWN = "UNKNOWN"
