from gymnasium import ActionWrapper


import logging


class BeaconAction(ActionWrapper):

    def action(self, action):
        beacons = []
        if len(action) == 0:
            beacons.append("WAIT")

        for i in range(len(action)):
            if action[i] > 0:
                beacons.append("BEACON {} {}".format(i, action[i]))

        act= ";".join(beacons)
        logging.debug(f'act : {act}')

        return act

    def reverse_action(self, action):
        return action