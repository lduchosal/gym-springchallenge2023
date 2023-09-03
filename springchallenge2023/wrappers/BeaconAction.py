from gymnasium import ActionWrapper


import logging


class BeaconAction(ActionWrapper):

    def action(self, action):
        beacons = []

        for i in range(len(action)):
            if action[i] > 0:
                a = int(action[i] * 1000)
                beacons.append("BEACON {} {}".format(i, a))

        if len(beacons) == 0:
            beacons.append("WAIT")

        act= ";".join(beacons)
        logging.debug(f'act : {act}')


        return act

    def reverse_action(self, action):
        return action