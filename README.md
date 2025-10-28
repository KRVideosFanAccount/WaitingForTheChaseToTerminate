Ever dreamed of expanding your **database** with new facts derived from meta-knowledge of your domain of application? The **chase algorithm** will take this additional knowledge into account to figure out more complete and relevant answers to your queries! Input your favorite **existential rules** and dataset, sit comfortably, and watch the chase as it operates its magic!*

\* *Disclaimer: This algorithm may take a while; please read Terms and Conditions before use. Excessive waiting for termination is dangerous for your health, run the chase with moderation.*

# Building the video

We recommend installing manim using `uv` as described in their documentation: https://docs.manim.community/en/stable/installation/uv.html .
To setup the environment, run 

``` shell
uv sync
```
Additionally, install Mononoki Nerd Font https://www.nerdfonts.com/font-downloads .

To render all scenes in 4k, run 

``` shell
source .venv/bin/activate
cd src
manim -qk scene_1.py && manim -qk scene_2.py && manim -qk scene_3.py Scene3_part1 Scene3_part2 Scene3_part3 && manim -qk scene_4.py && manim -qk scene_5.py && manim -qk scene_6.py && manim -qk scene_7.py
```

(Disclaimer: Rendering in parallel is discouraged, since the caching of the concurrent processes can interfere with each other.)

Open cut.kdenlive with kdenlive ( https://kdenlive.org/download/ ). If it complains about missing files, click on `Seach Recursively` and open the `src/media/` folder. 
To concatenate all scenes, use `Project -> Render...` to export the final video.

# Additional information

#### Summary of the video / Timecodes
00:00 Introduction & Intuition\
02:45 Framework & Definitions\
05:54 Fairness\
08:16 Termination & The Restricted Chase\
10:55 The Core Chase\
13:44 Recap' & Conclusion\
14:40 Credits\

#### How to cite:
https://doi.org/10.5281/zenodo.17456461

#### Manim:
https://www.manim.community/

#### KR website:
https://kr.org/

#### References:
- Jean-François Baget, Michel Leclère, Marie-Laure Mugnier, and Éric Salvat. On rules with existential variables: Walking the decidability line. Artificial Intelligence, 175(9-10):1620–1654, 2011.
- Catriel Beeri and Moshe Y. Vardi. The implication problem for data dependencies. In Proceedings of the 8th Colloquium on Automata, Languages and Programming, pages 73–85, 1981.
- David Carral, Lucas Larroque, Marie-Laure Mugnier, and Michaël Thomazo. Normalisations of Existential Rules: Not so Innocuous! In Proceedings of the 19th International Conference on Principles of Knowledge Representation and Reasoning (KR), pages 102–111, 2022.
