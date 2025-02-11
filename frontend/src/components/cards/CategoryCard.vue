<template>
    <div class="container" @click="navigate_to_category(category.category_name, category.category_id)"
        style="padding: .3rem;">
        <img class="imagen" :src="`${URI}/read-photo-product/${category.image_identifier}/600`">

        <div class="name-container" style="width: 100%;height: 40%; text-align: center;">
            <h3 class="name p-0 m-0" > {{ category.category_name?.toLowerCase() }}  </h3>
        </div>
    </div>
</template>

<script setup>
import { defineProps } from 'vue';
import router from '@/router';
import { URI } from '@/service/conection';

const navigate_to_category = (categor_name, category_id) => {
    router.push(`/categoria/${categor_name}/${category_id}`)
}

// Definir las props
const props = defineProps({
    category: {
        type: Object,
        required: true
    },
});
</script>

<style scoped>
.container {
    width: 100%;
    position: relative;
    height: 100%;
    transition: all ease 0.2s;
    overflow: hidden;
    display: flex !important;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    border-radius: .5rem;
    background-color: white;
    cursor: pointer;
    /* Añadido para asegurar que el pseudo-elemento quede detrás del contenido */
    z-index: 0;
    /* padding: 1rem; */

}

.container:hover{
    animation: rotateGradient 2s linear infinite;

}

.imagen {
    width: 100%;
    height: 100%;
    object-fit: cover;
    aspect-ratio: 4 / 3;
    transition: all ease 0.2s;
    border-radius: .3rem;
    
}

.container:hover>* {
    color: white;
}


*{border: none;}
.imagen:hover {
    /* filter: brightness(1.3); */
}




.name {
    /* padding: 0 2rem; */
    text-transform: capitalize;
    /* color: rgb(0, 0, 0); */
}

.name-container{
   
}
/* .container:hover > .name-container{
    text-transform: capitalize;display: flex;padding-bottom: 0rem; justify-content: center;align-items: end; position: absolute;bottom: 0;border: none;color: white; background:linear-gradient(to top,rgb(0, 0, 0), transparent);
} */

.container:hover > .name{
    color: white;
}

/* .container:hover{
    transform: scale(1.05);
} */




/* ----------------------
   Borde con degradado animado
---------------------- */




/* Keyframes para ir rotando la dirección del degradado */
@keyframes rotateGradient {
  0.000% {
    background: linear-gradient(0deg, var(--primary-color), blue);
  }
  0.278% {
    background: linear-gradient(1deg, var(--primary-color), blue);
  }
  0.556% {
    background: linear-gradient(2deg, var(--primary-color), blue);
  }
  0.833% {
    background: linear-gradient(3deg, var(--primary-color), blue);
  }
  1.111% {
    background: linear-gradient(4deg, var(--primary-color), blue);
  }
  1.389% {
    background: linear-gradient(5deg, var(--primary-color), blue);
  }
  1.667% {
    background: linear-gradient(6deg, var(--primary-color), blue);
  }
  1.944% {
    background: linear-gradient(7deg, var(--primary-color), blue);
  }
  2.222% {
    background: linear-gradient(8deg, var(--primary-color), blue);
  }
  2.500% {
    background: linear-gradient(9deg, var(--primary-color), blue);
  }
  2.778% {
    background: linear-gradient(10deg, var(--primary-color), blue);
  }
  3.056% {
    background: linear-gradient(11deg, var(--primary-color), blue);
  }
  3.333% {
    background: linear-gradient(12deg, var(--primary-color), blue);
  }
  3.611% {
    background: linear-gradient(13deg, var(--primary-color), blue);
  }
  3.889% {
    background: linear-gradient(14deg, var(--primary-color), blue);
  }
  4.167% {
    background: linear-gradient(15deg, var(--primary-color), blue);
  }
  4.444% {
    background: linear-gradient(16deg, var(--primary-color), blue);
  }
  4.722% {
    background: linear-gradient(17deg, var(--primary-color), blue);
  }
  5.000% {
    background: linear-gradient(18deg, var(--primary-color), blue);
  }
  5.278% {
    background: linear-gradient(19deg, var(--primary-color), blue);
  }
  5.556% {
    background: linear-gradient(20deg, var(--primary-color), blue);
  }
  5.833% {
    background: linear-gradient(21deg, var(--primary-color), blue);
  }
  6.111% {
    background: linear-gradient(22deg, var(--primary-color), blue);
  }
  6.389% {
    background: linear-gradient(23deg, var(--primary-color), blue);
  }
  6.667% {
    background: linear-gradient(24deg, var(--primary-color), blue);
  }
  6.944% {
    background: linear-gradient(25deg, var(--primary-color), blue);
  }
  7.222% {
    background: linear-gradient(26deg, var(--primary-color), blue);
  }
  7.500% {
    background: linear-gradient(27deg, var(--primary-color), blue);
  }
  7.778% {
    background: linear-gradient(28deg, var(--primary-color), blue);
  }
  8.056% {
    background: linear-gradient(29deg, var(--primary-color), blue);
  }
  8.333% {
    background: linear-gradient(30deg, var(--primary-color), blue);
  }
  8.611% {
    background: linear-gradient(31deg, var(--primary-color), blue);
  }
  8.889% {
    background: linear-gradient(32deg, var(--primary-color), blue);
  }
  9.167% {
    background: linear-gradient(33deg, var(--primary-color), blue);
  }
  9.444% {
    background: linear-gradient(34deg, var(--primary-color), blue);
  }
  9.722% {
    background: linear-gradient(35deg, var(--primary-color), blue);
  }
  10.000% {
    background: linear-gradient(36deg, var(--primary-color), blue);
  }
  10.278% {
    background: linear-gradient(37deg, var(--primary-color), blue);
  }
  10.556% {
    background: linear-gradient(38deg, var(--primary-color), blue);
  }
  10.833% {
    background: linear-gradient(39deg, var(--primary-color), blue);
  }
  11.111% {
    background: linear-gradient(40deg, var(--primary-color), blue);
  }
  11.389% {
    background: linear-gradient(41deg, var(--primary-color), blue);
  }
  11.667% {
    background: linear-gradient(42deg, var(--primary-color), blue);
  }
  11.944% {
    background: linear-gradient(43deg, var(--primary-color), blue);
  }
  12.222% {
    background: linear-gradient(44deg, var(--primary-color), blue);
  }
  12.500% {
    background: linear-gradient(45deg, var(--primary-color), blue);
  }
  12.778% {
    background: linear-gradient(46deg, var(--primary-color), blue);
  }
  13.056% {
    background: linear-gradient(47deg, var(--primary-color), blue);
  }
  13.333% {
    background: linear-gradient(48deg, var(--primary-color), blue);
  }
  13.611% {
    background: linear-gradient(49deg, var(--primary-color), blue);
  }
  13.889% {
    background: linear-gradient(50deg, var(--primary-color), blue);
  }
  14.167% {
    background: linear-gradient(51deg, var(--primary-color), blue);
  }
  14.444% {
    background: linear-gradient(52deg, var(--primary-color), blue);
  }
  14.722% {
    background: linear-gradient(53deg, var(--primary-color), blue);
  }
  15.000% {
    background: linear-gradient(54deg, var(--primary-color), blue);
  }
  15.278% {
    background: linear-gradient(55deg, var(--primary-color), blue);
  }
  15.556% {
    background: linear-gradient(56deg, var(--primary-color), blue);
  }
  15.833% {
    background: linear-gradient(57deg, var(--primary-color), blue);
  }
  16.111% {
    background: linear-gradient(58deg, var(--primary-color), blue);
  }
  16.389% {
    background: linear-gradient(59deg, var(--primary-color), blue);
  }
  16.667% {
    background: linear-gradient(60deg, var(--primary-color), blue);
  }
  16.944% {
    background: linear-gradient(61deg, var(--primary-color), blue);
  }
  17.222% {
    background: linear-gradient(62deg, var(--primary-color), blue);
  }
  17.500% {
    background: linear-gradient(63deg, var(--primary-color), blue);
  }
  17.778% {
    background: linear-gradient(64deg, var(--primary-color), blue);
  }
  18.056% {
    background: linear-gradient(65deg, var(--primary-color), blue);
  }
  18.333% {
    background: linear-gradient(66deg, var(--primary-color), blue);
  }
  18.611% {
    background: linear-gradient(67deg, var(--primary-color), blue);
  }
  18.889% {
    background: linear-gradient(68deg, var(--primary-color), blue);
  }
  19.167% {
    background: linear-gradient(69deg, var(--primary-color), blue);
  }
  19.444% {
    background: linear-gradient(70deg, var(--primary-color), blue);
  }
  19.722% {
    background: linear-gradient(71deg, var(--primary-color), blue);
  }
  20.000% {
    background: linear-gradient(72deg, var(--primary-color), blue);
  }
  20.278% {
    background: linear-gradient(73deg, var(--primary-color), blue);
  }
  20.556% {
    background: linear-gradient(74deg, var(--primary-color), blue);
  }
  20.833% {
    background: linear-gradient(75deg, var(--primary-color), blue);
  }
  21.111% {
    background: linear-gradient(76deg, var(--primary-color), blue);
  }
  21.389% {
    background: linear-gradient(77deg, var(--primary-color), blue);
  }
  21.667% {
    background: linear-gradient(78deg, var(--primary-color), blue);
  }
  21.944% {
    background: linear-gradient(79deg, var(--primary-color), blue);
  }
  22.222% {
    background: linear-gradient(80deg, var(--primary-color), blue);
  }
  22.500% {
    background: linear-gradient(81deg, var(--primary-color), blue);
  }
  22.778% {
    background: linear-gradient(82deg, var(--primary-color), blue);
  }
  23.056% {
    background: linear-gradient(83deg, var(--primary-color), blue);
  }
  23.333% {
    background: linear-gradient(84deg, var(--primary-color), blue);
  }
  23.611% {
    background: linear-gradient(85deg, var(--primary-color), blue);
  }
  23.889% {
    background: linear-gradient(86deg, var(--primary-color), blue);
  }
  24.167% {
    background: linear-gradient(87deg, var(--primary-color), blue);
  }
  24.444% {
    background: linear-gradient(88deg, var(--primary-color), blue);
  }
  24.722% {
    background: linear-gradient(89deg, var(--primary-color), blue);
  }
  25.000% {
    background: linear-gradient(90deg, var(--primary-color), blue);
  }
  25.278% {
    background: linear-gradient(91deg, var(--primary-color), blue);
  }
  25.556% {
    background: linear-gradient(92deg, var(--primary-color), blue);
  }
  25.833% {
    background: linear-gradient(93deg, var(--primary-color), blue);
  }
  26.111% {
    background: linear-gradient(94deg, var(--primary-color), blue);
  }
  26.389% {
    background: linear-gradient(95deg, var(--primary-color), blue);
  }
  26.667% {
    background: linear-gradient(96deg, var(--primary-color), blue);
  }
  26.944% {
    background: linear-gradient(97deg, var(--primary-color), blue);
  }
  27.222% {
    background: linear-gradient(98deg, var(--primary-color), blue);
  }
  27.500% {
    background: linear-gradient(99deg, var(--primary-color), blue);
  }
  27.778% {
    background: linear-gradient(100deg, var(--primary-color), blue);
  }
  28.056% {
    background: linear-gradient(101deg, var(--primary-color), blue);
  }
  28.333% {
    background: linear-gradient(102deg, var(--primary-color), blue);
  }
  28.611% {
    background: linear-gradient(103deg, var(--primary-color), blue);
  }
  28.889% {
    background: linear-gradient(104deg, var(--primary-color), blue);
  }
  29.167% {
    background: linear-gradient(105deg, var(--primary-color), blue);
  }
  29.444% {
    background: linear-gradient(106deg, var(--primary-color), blue);
  }
  29.722% {
    background: linear-gradient(107deg, var(--primary-color), blue);
  }
  30.000% {
    background: linear-gradient(108deg, var(--primary-color), blue);
  }
  30.278% {
    background: linear-gradient(109deg, var(--primary-color), blue);
  }
  30.556% {
    background: linear-gradient(110deg, var(--primary-color), blue);
  }
  30.833% {
    background: linear-gradient(111deg, var(--primary-color), blue);
  }
  31.111% {
    background: linear-gradient(112deg, var(--primary-color), blue);
  }
  31.389% {
    background: linear-gradient(113deg, var(--primary-color), blue);
  }
  31.667% {
    background: linear-gradient(114deg, var(--primary-color), blue);
  }
  31.944% {
    background: linear-gradient(115deg, var(--primary-color), blue);
  }
  32.222% {
    background: linear-gradient(116deg, var(--primary-color), blue);
  }
  32.500% {
    background: linear-gradient(117deg, var(--primary-color), blue);
  }
  32.778% {
    background: linear-gradient(118deg, var(--primary-color), blue);
  }
  33.056% {
    background: linear-gradient(119deg, var(--primary-color), blue);
  }
  33.333% {
    background: linear-gradient(120deg, var(--primary-color), blue);
  }
  33.611% {
    background: linear-gradient(121deg, var(--primary-color), blue);
  }
  33.889% {
    background: linear-gradient(122deg, var(--primary-color), blue);
  }
  34.167% {
    background: linear-gradient(123deg, var(--primary-color), blue);
  }
  34.444% {
    background: linear-gradient(124deg, var(--primary-color), blue);
  }
  34.722% {
    background: linear-gradient(125deg, var(--primary-color), blue);
  }
  35.000% {
    background: linear-gradient(126deg, var(--primary-color), blue);
  }
  35.278% {
    background: linear-gradient(127deg, var(--primary-color), blue);
  }
  35.556% {
    background: linear-gradient(128deg, var(--primary-color), blue);
  }
  35.833% {
    background: linear-gradient(129deg, var(--primary-color), blue);
  }
  36.111% {
    background: linear-gradient(130deg, var(--primary-color), blue);
  }
  36.389% {
    background: linear-gradient(131deg, var(--primary-color), blue);
  }
  36.667% {
    background: linear-gradient(132deg, var(--primary-color), blue);
  }
  36.944% {
    background: linear-gradient(133deg, var(--primary-color), blue);
  }
  37.222% {
    background: linear-gradient(134deg, var(--primary-color), blue);
  }
  37.500% {
    background: linear-gradient(135deg, var(--primary-color), blue);
  }
  37.778% {
    background: linear-gradient(136deg, var(--primary-color), blue);
  }
  38.056% {
    background: linear-gradient(137deg, var(--primary-color), blue);
  }
  38.333% {
    background: linear-gradient(138deg, var(--primary-color), blue);
  }
  38.611% {
    background: linear-gradient(139deg, var(--primary-color), blue);
  }
  38.889% {
    background: linear-gradient(140deg, var(--primary-color), blue);
  }
  39.167% {
    background: linear-gradient(141deg, var(--primary-color), blue);
  }
  39.444% {
    background: linear-gradient(142deg, var(--primary-color), blue);
  }
  39.722% {
    background: linear-gradient(143deg, var(--primary-color), blue);
  }
  40.000% {
    background: linear-gradient(144deg, var(--primary-color), blue);
  }
  40.278% {
    background: linear-gradient(145deg, var(--primary-color), blue);
  }
  40.556% {
    background: linear-gradient(146deg, var(--primary-color), blue);
  }
  40.833% {
    background: linear-gradient(147deg, var(--primary-color), blue);
  }
  41.111% {
    background: linear-gradient(148deg, var(--primary-color), blue);
  }
  41.389% {
    background: linear-gradient(149deg, var(--primary-color), blue);
  }
  41.667% {
    background: linear-gradient(150deg, var(--primary-color), blue);
  }
  41.944% {
    background: linear-gradient(151deg, var(--primary-color), blue);
  }
  42.222% {
    background: linear-gradient(152deg, var(--primary-color), blue);
  }
  42.500% {
    background: linear-gradient(153deg, var(--primary-color), blue);
  }
  42.778% {
    background: linear-gradient(154deg, var(--primary-color), blue);
  }
  43.056% {
    background: linear-gradient(155deg, var(--primary-color), blue);
  }
  43.333% {
    background: linear-gradient(156deg, var(--primary-color), blue);
  }
  43.611% {
    background: linear-gradient(157deg, var(--primary-color), blue);
  }
  43.889% {
    background: linear-gradient(158deg, var(--primary-color), blue);
  }
  44.167% {
    background: linear-gradient(159deg, var(--primary-color), blue);
  }
  44.444% {
    background: linear-gradient(160deg, var(--primary-color), blue);
  }
  44.722% {
    background: linear-gradient(161deg, var(--primary-color), blue);
  }
  45.000% {
    background: linear-gradient(162deg, var(--primary-color), blue);
  }
  45.278% {
    background: linear-gradient(163deg, var(--primary-color), blue);
  }
  45.556% {
    background: linear-gradient(164deg, var(--primary-color), blue);
  }
  45.833% {
    background: linear-gradient(165deg, var(--primary-color), blue);
  }
  46.111% {
    background: linear-gradient(166deg, var(--primary-color), blue);
  }
  46.389% {
    background: linear-gradient(167deg, var(--primary-color), blue);
  }
  46.667% {
    background: linear-gradient(168deg, var(--primary-color), blue);
  }
  46.944% {
    background: linear-gradient(169deg, var(--primary-color), blue);
  }
  47.222% {
    background: linear-gradient(170deg, var(--primary-color), blue);
  }
  47.500% {
    background: linear-gradient(171deg, var(--primary-color), blue);
  }
  47.778% {
    background: linear-gradient(172deg, var(--primary-color), blue);
  }
  48.056% {
    background: linear-gradient(173deg, var(--primary-color), blue);
  }
  48.333% {
    background: linear-gradient(174deg, var(--primary-color), blue);
  }
  48.611% {
    background: linear-gradient(175deg, var(--primary-color), blue);
  }
  48.889% {
    background: linear-gradient(176deg, var(--primary-color), blue);
  }
  49.167% {
    background: linear-gradient(177deg, var(--primary-color), blue);
  }
  49.444% {
    background: linear-gradient(178deg, var(--primary-color), blue);
  }
  49.722% {
    background: linear-gradient(179deg, var(--primary-color), blue);
  }
  50.000% {
    background: linear-gradient(180deg, var(--primary-color), blue);
  }
  50.278% {
    background: linear-gradient(181deg, var(--primary-color), blue);
  }
  50.556% {
    background: linear-gradient(182deg, var(--primary-color), blue);
  }
  50.833% {
    background: linear-gradient(183deg, var(--primary-color), blue);
  }
  51.111% {
    background: linear-gradient(184deg, var(--primary-color), blue);
  }
  51.389% {
    background: linear-gradient(185deg, var(--primary-color), blue);
  }
  51.667% {
    background: linear-gradient(186deg, var(--primary-color), blue);
  }
  51.944% {
    background: linear-gradient(187deg, var(--primary-color), blue);
  }
  52.222% {
    background: linear-gradient(188deg, var(--primary-color), blue);
  }
  52.500% {
    background: linear-gradient(189deg, var(--primary-color), blue);
  }
  52.778% {
    background: linear-gradient(190deg, var(--primary-color), blue);
  }
  53.056% {
    background: linear-gradient(191deg, var(--primary-color), blue);
  }
  53.333% {
    background: linear-gradient(192deg, var(--primary-color), blue);
  }
  53.611% {
    background: linear-gradient(193deg, var(--primary-color), blue);
  }
  53.889% {
    background: linear-gradient(194deg, var(--primary-color), blue);
  }
  54.167% {
    background: linear-gradient(195deg, var(--primary-color), blue);
  }
  54.444% {
    background: linear-gradient(196deg, var(--primary-color), blue);
  }
  54.722% {
    background: linear-gradient(197deg, var(--primary-color), blue);
  }
  55.000% {
    background: linear-gradient(198deg, var(--primary-color), blue);
  }
  55.278% {
    background: linear-gradient(199deg, var(--primary-color), blue);
  }
  55.556% {
    background: linear-gradient(200deg, var(--primary-color), blue);
  }
  55.833% {
    background: linear-gradient(201deg, var(--primary-color), blue);
  }
  56.111% {
    background: linear-gradient(202deg, var(--primary-color), blue);
  }
  56.389% {
    background: linear-gradient(203deg, var(--primary-color), blue);
  }
  56.667% {
    background: linear-gradient(204deg, var(--primary-color), blue);
  }
  56.944% {
    background: linear-gradient(205deg, var(--primary-color), blue);
  }
  57.222% {
    background: linear-gradient(206deg, var(--primary-color), blue);
  }
  57.500% {
    background: linear-gradient(207deg, var(--primary-color), blue);
  }
  57.778% {
    background: linear-gradient(208deg, var(--primary-color), blue);
  }
  58.056% {
    background: linear-gradient(209deg, var(--primary-color), blue);
  }
  58.333% {
    background: linear-gradient(210deg, var(--primary-color), blue);
  }
  58.611% {
    background: linear-gradient(211deg, var(--primary-color), blue);
  }
  58.889% {
    background: linear-gradient(212deg, var(--primary-color), blue);
  }
  59.167% {
    background: linear-gradient(213deg, var(--primary-color), blue);
  }
  59.444% {
    background: linear-gradient(214deg, var(--primary-color), blue);
  }
  59.722% {
    background: linear-gradient(215deg, var(--primary-color), blue);
  }
  60.000% {
    background: linear-gradient(216deg, var(--primary-color), blue);
  }
  60.278% {
    background: linear-gradient(217deg, var(--primary-color), blue);
  }
  60.556% {
    background: linear-gradient(218deg, var(--primary-color), blue);
  }
  60.833% {
    background: linear-gradient(219deg, var(--primary-color), blue);
  }
  61.111% {
    background: linear-gradient(220deg, var(--primary-color), blue);
  }
  61.389% {
    background: linear-gradient(221deg, var(--primary-color), blue);
  }
  61.667% {
    background: linear-gradient(222deg, var(--primary-color), blue);
  }
  61.944% {
    background: linear-gradient(223deg, var(--primary-color), blue);
  }
  62.222% {
    background: linear-gradient(224deg, var(--primary-color), blue);
  }
  62.500% {
    background: linear-gradient(225deg, var(--primary-color), blue);
  }
  62.778% {
    background: linear-gradient(226deg, var(--primary-color), blue);
  }
  63.056% {
    background: linear-gradient(227deg, var(--primary-color), blue);
  }
  63.333% {
    background: linear-gradient(228deg, var(--primary-color), blue);
  }
  63.611% {
    background: linear-gradient(229deg, var(--primary-color), blue);
  }
  63.889% {
    background: linear-gradient(230deg, var(--primary-color), blue);
  }
  64.167% {
    background: linear-gradient(231deg, var(--primary-color), blue);
  }
  64.444% {
    background: linear-gradient(232deg, var(--primary-color), blue);
  }
  64.722% {
    background: linear-gradient(233deg, var(--primary-color), blue);
  }
  65.000% {
    background: linear-gradient(234deg, var(--primary-color), blue);
  }
  65.278% {
    background: linear-gradient(235deg, var(--primary-color), blue);
  }
  65.556% {
    background: linear-gradient(236deg, var(--primary-color), blue);
  }
  65.833% {
    background: linear-gradient(237deg, var(--primary-color), blue);
  }
  66.111% {
    background: linear-gradient(238deg, var(--primary-color), blue);
  }
  66.389% {
    background: linear-gradient(239deg, var(--primary-color), blue);
  }
  66.667% {
    background: linear-gradient(240deg, var(--primary-color), blue);
  }
  66.944% {
    background: linear-gradient(241deg, var(--primary-color), blue);
  }
  67.222% {
    background: linear-gradient(242deg, var(--primary-color), blue);
  }
  67.500% {
    background: linear-gradient(243deg, var(--primary-color), blue);
  }
  67.778% {
    background: linear-gradient(244deg, var(--primary-color), blue);
  }
  68.056% {
    background: linear-gradient(245deg, var(--primary-color), blue);
  }
  68.333% {
    background: linear-gradient(246deg, var(--primary-color), blue);
  }
  68.611% {
    background: linear-gradient(247deg, var(--primary-color), blue);
  }
  68.889% {
    background: linear-gradient(248deg, var(--primary-color), blue);
  }
  69.167% {
    background: linear-gradient(249deg, var(--primary-color), blue);
  }
  69.444% {
    background: linear-gradient(250deg, var(--primary-color), blue);
  }
  69.722% {
    background: linear-gradient(251deg, var(--primary-color), blue);
  }
  70.000% {
    background: linear-gradient(252deg, var(--primary-color), blue);
  }
  70.278% {
    background: linear-gradient(253deg, var(--primary-color), blue);
  }
  70.556% {
    background: linear-gradient(254deg, var(--primary-color), blue);
  }
  70.833% {
    background: linear-gradient(255deg, var(--primary-color), blue);
  }
  71.111% {
    background: linear-gradient(256deg, var(--primary-color), blue);
  }
  71.389% {
    background: linear-gradient(257deg, var(--primary-color), blue);
  }
  71.667% {
    background: linear-gradient(258deg, var(--primary-color), blue);
  }
  71.944% {
    background: linear-gradient(259deg, var(--primary-color), blue);
  }
  72.222% {
    background: linear-gradient(260deg, var(--primary-color), blue);
  }
  72.500% {
    background: linear-gradient(261deg, var(--primary-color), blue);
  }
  72.778% {
    background: linear-gradient(262deg, var(--primary-color), blue);
  }
  73.056% {
    background: linear-gradient(263deg, var(--primary-color), blue);
  }
  73.333% {
    background: linear-gradient(264deg, var(--primary-color), blue);
  }
  73.611% {
    background: linear-gradient(265deg, var(--primary-color), blue);
  }
  73.889% {
    background: linear-gradient(266deg, var(--primary-color), blue);
  }
  74.167% {
    background: linear-gradient(267deg, var(--primary-color), blue);
  }
  74.444% {
    background: linear-gradient(268deg, var(--primary-color), blue);
  }
  74.722% {
    background: linear-gradient(269deg, var(--primary-color), blue);
  }
  75.000% {
    background: linear-gradient(270deg, var(--primary-color), blue);
  }
  75.278% {
    background: linear-gradient(271deg, var(--primary-color), blue);
  }
  75.556% {
    background: linear-gradient(272deg, var(--primary-color), blue);
  }
  75.833% {
    background: linear-gradient(273deg, var(--primary-color), blue);
  }
  76.111% {
    background: linear-gradient(274deg, var(--primary-color), blue);
  }
  76.389% {
    background: linear-gradient(275deg, var(--primary-color), blue);
  }
  76.667% {
    background: linear-gradient(276deg, var(--primary-color), blue);
  }
  76.944% {
    background: linear-gradient(277deg, var(--primary-color), blue);
  }
  77.222% {
    background: linear-gradient(278deg, var(--primary-color), blue);
  }
  77.500% {
    background: linear-gradient(279deg, var(--primary-color), blue);
  }
  77.778% {
    background: linear-gradient(280deg, var(--primary-color), blue);
  }
  78.056% {
    background: linear-gradient(281deg, var(--primary-color), blue);
  }
  78.333% {
    background: linear-gradient(282deg, var(--primary-color), blue);
  }
  78.611% {
    background: linear-gradient(283deg, var(--primary-color), blue);
  }
  78.889% {
    background: linear-gradient(284deg, var(--primary-color), blue);
  }
  79.167% {
    background: linear-gradient(285deg, var(--primary-color), blue);
  }
  79.444% {
    background: linear-gradient(286deg, var(--primary-color), blue);
  }
  79.722% {
    background: linear-gradient(287deg, var(--primary-color), blue);
  }
  80.000% {
    background: linear-gradient(288deg, var(--primary-color), blue);
  }
  80.278% {
    background: linear-gradient(289deg, var(--primary-color), blue);
  }
  80.556% {
    background: linear-gradient(290deg, var(--primary-color), blue);
  }
  80.833% {
    background: linear-gradient(291deg, var(--primary-color), blue);
  }
  81.111% {
    background: linear-gradient(292deg, var(--primary-color), blue);
  }
  81.389% {
    background: linear-gradient(293deg, var(--primary-color), blue);
  }
  81.667% {
    background: linear-gradient(294deg, var(--primary-color), blue);
  }
  81.944% {
    background: linear-gradient(295deg, var(--primary-color), blue);
  }
  82.222% {
    background: linear-gradient(296deg, var(--primary-color), blue);
  }
  82.500% {
    background: linear-gradient(297deg, var(--primary-color), blue);
  }
  82.778% {
    background: linear-gradient(298deg, var(--primary-color), blue);
  }
  83.056% {
    background: linear-gradient(299deg, var(--primary-color), blue);
  }
  83.333% {
    background: linear-gradient(300deg, var(--primary-color), blue);
  }
  83.611% {
    background: linear-gradient(301deg, var(--primary-color), blue);
  }
  83.889% {
    background: linear-gradient(302deg, var(--primary-color), blue);
  }
  84.167% {
    background: linear-gradient(303deg, var(--primary-color), blue);
  }
  84.444% {
    background: linear-gradient(304deg, var(--primary-color), blue);
  }
  84.722% {
    background: linear-gradient(305deg, var(--primary-color), blue);
  }
  85.000% {
    background: linear-gradient(306deg, var(--primary-color), blue);
  }
  85.278% {
    background: linear-gradient(307deg, var(--primary-color), blue);
  }
  85.556% {
    background: linear-gradient(308deg, var(--primary-color), blue);
  }
  85.833% {
    background: linear-gradient(309deg, var(--primary-color), blue);
  }
  86.111% {
    background: linear-gradient(310deg, var(--primary-color), blue);
  }
  86.389% {
    background: linear-gradient(311deg, var(--primary-color), blue);
  }
  86.667% {
    background: linear-gradient(312deg, var(--primary-color), blue);
  }
  86.944% {
    background: linear-gradient(313deg, var(--primary-color), blue);
  }
  87.222% {
    background: linear-gradient(314deg, var(--primary-color), blue);
  }
  87.500% {
    background: linear-gradient(315deg, var(--primary-color), blue);
  }
  87.778% {
    background: linear-gradient(316deg, var(--primary-color), blue);
  }
  88.056% {
    background: linear-gradient(317deg, var(--primary-color), blue);
  }
  88.333% {
    background: linear-gradient(318deg, var(--primary-color), blue);
  }
  88.611% {
    background: linear-gradient(319deg, var(--primary-color), blue);
  }
  88.889% {
    background: linear-gradient(320deg, var(--primary-color), blue);
  }
  89.167% {
    background: linear-gradient(321deg, var(--primary-color), blue);
  }
  89.444% {
    background: linear-gradient(322deg, var(--primary-color), blue);
  }
  89.722% {
    background: linear-gradient(323deg, var(--primary-color), blue);
  }
  90.000% {
    background: linear-gradient(324deg, var(--primary-color), blue);
  }
  90.278% {
    background: linear-gradient(325deg, var(--primary-color), blue);
  }
  90.556% {
    background: linear-gradient(326deg, var(--primary-color), blue);
  }
  90.833% {
    background: linear-gradient(327deg, var(--primary-color), blue);
  }
  91.111% {
    background: linear-gradient(328deg, var(--primary-color), blue);
  }
  91.389% {
    background: linear-gradient(329deg, var(--primary-color), blue);
  }
  91.667% {
    background: linear-gradient(330deg, var(--primary-color), blue);
  }
  91.944% {
    background: linear-gradient(331deg, var(--primary-color), blue);
  }
  92.222% {
    background: linear-gradient(332deg, var(--primary-color), blue);
  }
  92.500% {
    background: linear-gradient(333deg, var(--primary-color), blue);
  }
  92.778% {
    background: linear-gradient(334deg, var(--primary-color), blue);
  }
  93.056% {
    background: linear-gradient(335deg, var(--primary-color), blue);
  }
  93.333% {
    background: linear-gradient(336deg, var(--primary-color), blue);
  }
  93.611% {
    background: linear-gradient(337deg, var(--primary-color), blue);
  }
  93.889% {
    background: linear-gradient(338deg, var(--primary-color), blue);
  }
  94.167% {
    background: linear-gradient(339deg, var(--primary-color), blue);
  }
  94.444% {
    background: linear-gradient(340deg, var(--primary-color), blue);
  }
  94.722% {
    background: linear-gradient(341deg, var(--primary-color), blue);
  }
  95.000% {
    background: linear-gradient(342deg, var(--primary-color), blue);
  }
  95.278% {
    background: linear-gradient(343deg, var(--primary-color), blue);
  }
  95.556% {
    background: linear-gradient(344deg, var(--primary-color), blue);
  }
  95.833% {
    background: linear-gradient(345deg, var(--primary-color), blue);
  }
  96.111% {
    background: linear-gradient(346deg, var(--primary-color), blue);
  }
  96.389% {
    background: linear-gradient(347deg, var(--primary-color), blue);
  }
  96.667% {
    background: linear-gradient(348deg, var(--primary-color), blue);
  }
  96.944% {
    background: linear-gradient(349deg, var(--primary-color), blue);
  }
  97.222% {
    background: linear-gradient(350deg, var(--primary-color), blue);
  }
  97.500% {
    background: linear-gradient(351deg, var(--primary-color), blue);
  }
  97.778% {
    background: linear-gradient(352deg, var(--primary-color), blue);
  }
  98.056% {
    background: linear-gradient(353deg, var(--primary-color), blue);
  }
  98.333% {
    background: linear-gradient(354deg, var(--primary-color), blue);
  }
  98.611% {
    background: linear-gradient(355deg, var(--primary-color), blue);
  }
  98.889% {
    background: linear-gradient(356deg, var(--primary-color), blue);
  }
  99.167% {
    background: linear-gradient(357deg, var(--primary-color), blue);
  }
  99.444% {
    background: linear-gradient(358deg, var(--primary-color), blue);
  }
  99.722% {
    background: linear-gradient(359deg, var(--primary-color), blue);
  }
  100.000% {
    background: linear-gradient(360deg, var(--primary-color), blue);
  }
}



@media (width < 740px) {
    .container {
        grid-template-columns: repeat(2, 1fr);
        gap: .5rem;
        padding: 1rem;
    }

    .name {
        font-size: 2rem;
        padding: 1rem;
  
    }
}

@media (width < 600px) {
    .container {
        grid-template-columns: repeat(2, 1fr);
        gap: .5rem;
        padding: 1rem;
    }

    .name {
        font-size: 2rem;
        padding: 1rem;
    }
}
</style>
