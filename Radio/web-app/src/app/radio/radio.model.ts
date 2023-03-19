export class Radio {
    constructor(
        public volume: number,
        public stream: string,
        public button_on_off: boolean,
        public button_lang: boolean,
        public button_mittel: boolean,
        public button_kurz: boolean,
        public button_ukw: boolean,
        public button_spr: boolean,
        public pos_lang_mittel_kurz: number,
        public pos_ukw_spr: number,
        public radio_name: string,
    ) {}
  }