import syllables

class Functions:

    def is_a_haiku(self, incoming):
        haiku = False
        words = str(incoming).split()

        syl_count = 0
        for word in words:
            syl_count += syllables.estimate(word)

        if syl_count == 17:
            line = ""
            lines = []
            syl_count = 0

            for word in words:
                syl_count += syllables.estimate(word)

                line = line + word + " "

                if len(lines) == 0 and syl_count == 5:
                    lines.append(line)
                    line = ""
                    syl_count = 0
                elif len(lines) == 0 and syl_count > 5:
                    break

                if len(lines) == 1 and syl_count == 7:
                    lines.append(line)
                    line = ""
                    syl_count = 0
                elif len(lines) == 1 and syl_count > 7:
                    break

                if len(lines) == 2 and syl_count == 5:
                    lines.append(line)
                    line = ""
                    haiku = True
                elif len(lines) == 2 and syl_count > 5:
                    break

        if haiku:
            return "\n".join(lines)
        else:
            return False
