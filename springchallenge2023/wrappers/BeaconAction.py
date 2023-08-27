from gymnasium import ActionWrapper


import logging


class BeaconAction(ActionWrapper):

    def action(self, action):
        beacons = []

        for i in range(len(action)):
            if action[i] > 0:
                beacons.append("BEACON {} {}".format(i, action[i]))

        if len(beacons) == 0:
            beacons.append("WAIT")

        act= ";".join(beacons)
        logging.debug(f'act : {act}')


        return act

    def reverse_action(self, action):
        return action