IF NOT EXISTS sports.trades
(
    trade_id serial NOT NULL,
    season_id integer NOT NULL,
    trade_date timestamp with time zone NOT NULL DEFAULT now(),
    initiating_team_id integer,
    deadline_trade boolean NOT NULL DEFAULT false,
    notes text COLLATE pg_catalog."default",
    metadata jsonb,
    trade_status_id integer NOT NULL,
    trade_type_id integer NOT NULL,
    CONSTRAINT trades_pkey PRIMARY KEY (trade_id)
);

ALTER TABLE IF EXISTS sports.athlete_sports
    ADD CONSTRAINT athlete_sports_athlete_id_fkey FOREIGN KEY (athlete_id)
    REFERENCES sports.athletes (athlete_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS sports.athlete_sports
    ADD CONSTRAINT athlete_sports_sport_id_fkey FOREIGN KEY (sport_id)
    REFERENCES sports.sports (sport_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS sports.athletes
    ADD CONSTRAINT athletes_country_id_fkey FOREIGN KEY (country_id)
    REFERENCES sports.reference_values (reference_value_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS sports.athletes_history
    ADD CONSTRAINT athletes_history_country_id_fkey FOREIGN KEY (country_id)
    REFERENCES sports.reference_values (reference_value_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS sports.contracts
    ADD CONSTRAINT contracts_athlete_id_fkey FOREIGN KEY (athlete_id)
    REFERENCES sports.athletes (athlete_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS sports.contracts
    ADD CONSTRAINT contracts_end_season_id_fkey FOREIGN KEY (end_season_id)
    REFERENCES sports.seasons (season_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS sports.contracts
    ADD CONSTRAINT contracts_start_season_id_fkey FOREIGN KEY (start_season_id)
    REFERENCES sports.seasons (season_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS sports.contracts
    ADD CONSTRAINT contracts_team_id_fkey FOREIGN KEY (team_id)
    REFERENCES sports.teams (team_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS sports.contracts
    ADD CONSTRAINT fk_contracts_type FOREIGN KEY (contract_type_id)
    REFERENCES sports.reference_values (reference_value_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS sports.game_metrics
    ADD CONSTRAINT fk_game_metrics_stat_definitions FOREIGN KEY (stat_def_id)
    REFERENCES sports.stat_definitions (stat_def_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS sports.game_metrics
    ADD CONSTRAINT game_metrics_game_id_fkey FOREIGN KEY (game_id)
    REFERENCES sports.games (game_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS sports.game_results
    ADD CONSTRAINT game_results_game_id_fkey FOREIGN KEY (game_id)
    REFERENCES sports.games (game_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;
CREATE INDEX IF NOT EXISTS game_results_pkey
    ON sports.game_results(game_id);


ALTER TABLE IF EXISTS sports.game_results
    ADD CONSTRAINT game_results_winning_team_id_fkey FOREIGN KEY (winning_team_id)
    REFERENCES sports.teams (team_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS sports.games
    ADD CONSTRAINT fk_away_team FOREIGN KEY (away_team_id)
    REFERENCES sports.teams (team_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS sports.games
    ADD CONSTRAINT fk_home_team FOREIGN KEY (home_team_id)
    REFERENCES sports.teams (team_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS sports.games
    ADD CONSTRAINT fk_season FOREIGN KEY (season_id)
    REFERENCES sports.seasons (season_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS sports.games
    ADD CONSTRAINT games_away_team_id_fkey FOREIGN KEY (away_team_id)
    REFERENCES sports.teams (team_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS sports.games
    ADD CONSTRAINT games_home_team_id_fkey FOREIGN KEY (home_team_id)
    REFERENCES sports.teams (team_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS sports.games
    ADD CONSTRAINT games_season_id_fkey FOREIGN KEY (season_id)
    REFERENCES sports.seasons (season_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS sports.leagues
    ADD CONSTRAINT fk_country FOREIGN KEY (country_id)
    REFERENCES sports.reference_values (reference_value_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS sports.leagues
    ADD CONSTRAINT fk_sport FOREIGN KEY (sport_id)
    REFERENCES sports.sports (sport_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;
CREATE INDEX IF NOT EXISTS idx_leagues_sport
    ON sports.leagues(sport_id);


ALTER TABLE IF EXISTS sports.player_game_stats
    ADD CONSTRAINT player_game_stats_athlete_id_fkey FOREIGN KEY (athlete_id)
    REFERENCES sports.athletes (athlete_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;
CREATE INDEX IF NOT EXISTS idx_stats_athlete
    ON sports.player_game_stats(athlete_id);


ALTER TABLE IF EXISTS sports.player_game_stats
    ADD CONSTRAINT player_game_stats_game_id_fkey FOREIGN KEY (game_id)
    REFERENCES sports.games (game_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;
CREATE INDEX IF NOT EXISTS idx_stats_game
    ON sports.player_game_stats(game_id);


ALTER TABLE IF EXISTS sports.player_game_stats
    ADD CONSTRAINT player_game_stats_roster_id_fkey FOREIGN KEY (roster_id)
    REFERENCES sports.rosters (roster_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;
CREATE INDEX IF NOT EXISTS idx_stats_roster
    ON sports.player_game_stats(roster_id);


ALTER TABLE IF EXISTS sports.player_game_stats
    ADD CONSTRAINT player_game_stats_stat_def_id_fkey FOREIGN KEY (stat_def_id)
    REFERENCES sports.stat_definitions (stat_def_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS sports.positions
    ADD CONSTRAINT fk_sport FOREIGN KEY (sport_id)
    REFERENCES sports.sports (sport_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;
CREATE INDEX IF NOT EXISTS idx_positions_sport
    ON sports.positions(sport_id);


ALTER TABLE IF EXISTS sports.reference_values
    ADD CONSTRAINT reference_values_reference_category_id_fkey FOREIGN KEY (reference_category_id)
    REFERENCES sports.reference_categories (reference_category_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS sports.roster_positions
    ADD CONSTRAINT fk_position FOREIGN KEY (position_id)
    REFERENCES sports.positions (position_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS sports.roster_positions
    ADD CONSTRAINT fk_roster FOREIGN KEY (roster_id)
    REFERENCES sports.rosters (roster_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS sports.rosters
    ADD CONSTRAINT fk_athlete FOREIGN KEY (athlete_id)
    REFERENCES sports.athletes (athlete_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS sports.rosters
    ADD CONSTRAINT fk_contracts FOREIGN KEY (contract_id)
    REFERENCES sports.contracts (contract_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS sports.rosters
    ADD CONSTRAINT fk_season FOREIGN KEY (season_id)
    REFERENCES sports.seasons (season_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS sports.rosters
    ADD CONSTRAINT fk_team FOREIGN KEY (team_id)
    REFERENCES sports.teams (team_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS sports.seasons
    ADD CONSTRAINT fk_league FOREIGN KEY (league_id)
    REFERENCES sports.leagues (league_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;
CREATE INDEX IF NOT EXISTS idx_seasons_league
    ON sports.seasons(league_id);


ALTER TABLE IF EXISTS sports.sports
    ADD CONSTRAINT fk_category FOREIGN KEY (category_id)
    REFERENCES sports.reference_values (reference_value_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;
CREATE INDEX IF NOT EXISTS idx_sports_category
    ON sports.sports(category_id);


ALTER TABLE IF EXISTS sports.stat_definitions
    ADD CONSTRAINT stat_definitions_sport_id_fkey FOREIGN KEY (sport_id)
    REFERENCES sports.sports (sport_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS sports.teams
    ADD CONSTRAINT fk_league FOREIGN KEY (league_id)
    REFERENCES sports.leagues (league_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;
CREATE INDEX IF NOT EXISTS idx_teams_league
    ON sports.teams(league_id);


ALTER TABLE IF EXISTS sports.trade_teams
    ADD CONSTRAINT trade_teams_team_id_fkey FOREIGN KEY (team_id)
    REFERENCES sports.teams (team_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS sports.trade_teams
    ADD CONSTRAINT trade_teams_trade_id_fkey FOREIGN KEY (trade_id)
    REFERENCES sports.trades (trade_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS sports.trade_teams
    ADD CONSTRAINT trade_teams_trade_team_role_id_fkey FOREIGN KEY (trade_team_role_id)
    REFERENCES sports.reference_values (reference_value_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS sports.trades
    ADD CONSTRAINT trades_initiating_team_id_fkey FOREIGN KEY (initiating_team_id)
    REFERENCES sports.teams (team_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS sports.trades
    ADD CONSTRAINT trades_season_id_fkey FOREIGN KEY (season_id)
    REFERENCES sports.seasons (season_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS sports.trades
    ADD CONSTRAINT trades_trade_status_id_fkey FOREIGN KEY (trade_status_id)
    REFERENCES sports.reference_values (reference_value_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS sports.trades
    ADD CONSTRAINT trades_trade_type_id_fkey FOREIGN KEY (trade_type_id)
    REFERENCES sports.reference_values (reference_value_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;

END