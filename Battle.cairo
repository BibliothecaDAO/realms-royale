// amarna: disable=arithmetic-add,arithmetic-div,arithmetic-mul,arithmetic-sub
// -----------------------------------
//
// MIT License
// -----------------------------------

%lang starknet

from starkware.cairo.common.alloc import alloc
from starkware.cairo.common.cairo_builtins import HashBuiltin, BitwiseBuiltin
from starkware.cairo.common.bool import TRUE, FALSE
from starkware.cairo.common.uint256 import Uint256, uint256_unsigned_div_rem
from starkware.starknet.common.syscalls import get_block_timestamp, get_caller_address
from starkware.cairo.common.math import unsigned_div_rem
from starkware.cairo.common.math_cmp import is_le, is_not_zero

from openzeppelin.upgrades.library import Proxy

// -----------------------------------
// Initialize & upgrade
// -----------------------------------

// @notice Module initializer
// @param address_of_controller: Controller/arbiter address
// @return proxy_admin: Proxy admin address
@external
func initializer{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    proxy_admin: felt
) {
    Proxy.initializer(proxy_admin);
    return ();
}

// @notice Set new proxy implementation
// @dev Can only be set by the arbiter
// @param new_implementation: New implementation contract address
@external
func upgrade{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    new_implementation: felt
) {
    Proxy.assert_only_admin();
    Proxy._set_implementation_hash(new_implementation);
    return ();
}

struct PlayerInformation {
    location: felt,
    unit_id: felt,
}

struct Game {
    public_key: felt,
    p_1: felt,
    p_2: felt,
    p_3: felt,
}

@storage_var
func turn(game_id: felt) -> (player: felt) {
}

@storage_var
func game_counter() -> (game_number: felt) {
}

@storage_var
func game_details(game_id: felt) -> (game: Game) {
}

@storage_var
func location(game_id: felt, location_hash: felt) -> (player_id: felt) {
}

@storage_var
func player(game_id: felt, player_id: felt) -> (location: felt) {
}

@external
func moveToKill{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    game_id: felt, player_id: felt, location_hash: felt
) -> (killed_id: felt) {
    alloc_locals;
    // check move
    let (current_turn) = turn.read(game_id);

    with_attr error_message("NOT YOUR TURN") {
        assert current_turn = player_id;
    }

    // get current location - 0 for nothing. 1,2,3 indicates players.
    let (current_location_player_id) = location.read(game_id, location_hash);

    // kill the player if one exists at this location - 666 means in hell.
    // TODO: this should be bool, otherwise we are needlessly writing....
    player.write(game_id, current_location_player_id, 666);

    // clear current location move - 0 is blank
    let (player_location) = player.read(game_id, player_id);

    if (player_location == 666) {
        with_attr error_message("YOU ARE IN HELL") {
            assert 0 = 1;
        }
    }

    location.write(game_id, player_location, 0);

    // move player to new location
    location.write(game_id, location_hash, player_id);
    player.write(game_id, player_id, location_hash);

    // next turn
    if (player_id == 1) {
        turn.write(game_id, player_id + 1);
        return (current_location_player_id,);
    }
    if (player_id == 2) {
        turn.write(game_id, player_id + 1);
        return (current_location_player_id,);
    }
    if (player_id == 3) {
        turn.write(game_id, 1);
        return (current_location_player_id,);
    }
    return (0,);
}

@external
func create_game{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    public_key: felt
) -> (game_id: felt) {
    let (caller) = get_caller_address();
    let (current_game) = game_counter.read();

    tempvar next_game = current_game + 1;

    game_counter.write(next_game);

    let exists = is_not_zero(public_key);

    assert exists = TRUE;

    // set creator as player 1
    game_details.write(next_game, Game(public_key, caller, 0, 0));

    return (game_id=next_game);
}

@external
func join_game{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(game_id: felt) -> (
    game_id: felt
) {
    let (caller) = get_caller_address();
    let (current_game) = game_details.read(game_id);

    let p1_exists = is_not_zero(current_game.p_1);

    with_attr error_message("GAME DOES NOT EXIST") {
        assert p1_exists = TRUE;
    }

    if (current_game.p_2 == 0) {
        game_details.write(game_id, Game(current_game.public_key, current_game.p_1, caller, 0));
        return (game_id,);
    }

    if (current_game.p_3 == 0) {
        game_details.write(
            game_id, Game(current_game.public_key, current_game.p_1, current_game.p_2, caller)
        );
        // sets player 1s turn
        turn.write(game_id, 1);
        return (game_id,);
    }

    return (game_id,);
}
